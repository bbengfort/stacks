# books.gbs
# Google Books API client
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Fri May 16 20:48:33 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: gbs.py [] benjamin@bengfort.com $

"""
Google Books API client
"""

##########################################################################
## Imports
##########################################################################

import requests

from urllib import urlencode
from stacks.utils.title import *
from datetime import datetime

##########################################################################
## Exception class
##########################################################################


class GoogleBooksException(Exception):
    """
    Abstract class to deal with Google Books errors.
    """
    pass

##########################################################################
## Query Builder
##########################################################################


class QueryBuilder(object):
    """
    Helper to dynamically construct a Google Books search query, both from
    init and at runtime.
    A Google Books search query is constructed of search terms and keyword
    search terms.
    Search terms are searched throughout the search space of the book,
    title, author, etc.
    Keyword search terms restrict the search to particular fields, those
    which I will allow are listed in the KEYWORDS class variable.
    """

    KEYWORDS = (
        'intitle',
        'inauthor',
        'inpublisher',
        'subject',
        'isbn',
        'lccn',
        'oclc',
    )

    def __init__(self, *terms, **kwterms):
        """
        Construct a query from terms and keyword terms.
        """

        # Init instance variables
        self.terms   = []
        self.kwterms = {}

        # Add the passed arguments
        for term in terms:
            self.add_term(term)
        for keyword, term in kwterms.items():
            self.add_keyword_term(keyword, term)

    def add_term(self, term):
        """
        Add a unique term to the query.
        """
        for t in self.terms:
            if t == term:
                return
        self.terms.append(term)

    def add_keyword_term(self, keyword, term):
        """
        Add a keyword term to the query
        """
        if keyword not in QueryBuilder.KEYWORDS:
            raise GoogleBooksException('%s is not a valid keyword' % keyword)

        if keyword in self.kwterms:
            self.kwterms[keyword] = '+'.join([self.kwterms[keyword], term])
        else:
            self.kwterms[keyword] = term

    # The following are aliases for constructing the query string.
    @property
    def query(self):
        """
        Property alias to initiate the query string construction
        """
        return self.get_query_string()

    def get_query_string(self):
        """
        Construct the query string and return.
        """
        q = "+".join(self.terms)

        for k, t in self.kwterms.items():
            if q != '':
                q = "+".join([q, "%s:%s" % (k, t)])
            else:
                q = "%s:%s" % (k, t)

        return q

    def __str__(self):
        return self.query

    def __unicode__(self):
        return self.query

##########################################################################
## API Access object
##########################################################################


class GoogleBooks(object):

    ENDPOINT = "https://www.googleapis.com/books/v1/volumes"

    def __init__(self, apikey=None, **kwargs):

        # add in the API key
        self.apikey = apikey

        # add any additional parameters to query or orverride defaults:
        for (k, v) in kwargs.iteritems():
            setattr(self, k, v)

    def lookup(self, query):
        """
        Executes a lookup request for the given QueryBuilder query
        Returns one of the following:
            - None (for nothing found)
            - A single dictionary (for one item found)
            - A list of dictionaries (for multiple items found)
        Note: GoogleBooksExceptions raised in parse will be caught,
        and none will be returned instead. Directly parse to debug.
        """
        params = {'q':query}
        response = self.execute(params)

        # Check for an Error
        if "error" in response:
            if "errors" in response["error"]:
                errors = response["error"]["errors"]
                if len(errors) > 0:
                    if "message" in errors[0]:
                        raise GoogleBooksException(errors[0]["message"])
            raise GoogleBooksException("Unknown error response from Google")
        # No error: return "relevant" data
        else:

            if "totalItems" in response:
                count = response["totalItems"]

                if count == 0:
                    return None
                else:
                    if "items" in response:
                        items = response["items"]
                    else:
                        raise GoogleBooksException("Unknown API error: could not find items in response.")

                if count > 1:
                    # Return a list of the items returned.
                    # TODO: case where there are multiple pages of results
                    books = [ ]

                    for item in items:
                        try:
                            books.append(BookDict(item))
                        except GoogleBooksException:
                            continue

                    if len(books) > 0:
                        return books
                    else:
                        return None

                elif count == 1:
                    # Return a single item, some queries expect this, e.g. isbn queries
                    try:
                        return BookDict(items[0])
                    except GoogleBooksException:
                        return None
                else:
                    # Total count was 0 or negative
                    return None

            else:
                raise GoogleBooksException("Unkown API error: no total item count in response.")

    def get_required_params(self):
        """
        Returns a dictionary of the parameters that must be added to the
        query.
        """
        if self.apikey:
            return {
                "key": self.apikey,
            }

        return {}

    def execute(self, params):
        """
        Execute an HTTP request with the given parameters
        """
        # create parameters string
        request = self.get_required_params()    # Create a request dictionary of required params
        request.update(params)                  # Update required params with passed in params
        request = urlencode(request)            # Percent escape and encode the request dictionary

        response = requests.get('?'.join([self.ENDPOINT, request]))
        return response.json()

##########################################################################
## Response Parser
##########################################################################


class BookDict(object):
    """
    Emulates a Query dictionary and wraps the returned JSON data from a
    Google Books Lookup. This class parses out the data for use in other
    applications, and decides what is "relevant" to our application.
    """

    def __init__(self, item_data):
        """
        Requires a python dictionary converted from Google Books JSON,
        specifically the item (not the items list or whole JSON).
        """
        self.raw_data = item_data
        self.item     = self.parse(item_data)

    @property
    def isbn(self):
        """
        Searches the "industryIdentifiers" field for the most relevant
        ISBN -- looks for ISBN_13, but returns ISBN_10 if it can't find it.
        """

        identifiers = self["industryIdentifiers"]
        searchkeys  = ("ISBN_13", "ISBN_10")        # Order matters here, the first one is the priority!
        return self.isbn_search(identifiers, searchkeys)

    @property
    def shortisbn(self):
        """
        Searches for ISBN_10 in "industryIdentifiers"
        """
        identifiers = self["industryIdentifiers"]
        return self.isbn_search(identifiers, ("ISBN_10",))

    @property
    def title(self):
        """
        Alias for self['title']
        """
        return make_title(self['title'])

    @property
    def authors(self):
        """
        Generator function that yields all the authors in the authors
        field.
        This could simply be an alias for self['authors'] but if we want
        to do any management or memory optimization, this functionality
        will be helpful
        Note: Currently yields full name strings.
        """
        if self['authors']:
            for author in self['authors']:
                yield author

    @property
    def publisher(self):
        """
        Alias for self['publisher']. Yields publisher name.
        """
        return self['publisher']

    @property
    def pubdate(self):
        """
        Converts "publishedDate" into a python date
        If a publishedDate couldn't be found or parsed, this method will
        return None.
        """

        published = self["publishedDate"]

        datefmts = ("%Y-%m-%d", "%Y-%m", "%Y")
        for fmt in datefmts:
            try:
                dt = datetime.strptime(published, fmt)
                return dt.date()
            except ValueError:
                # If ValueError, then this format didn't work, try the next.
                continue
            except TypeError:
                # If TypeError, then published is probably None, so break and return.
                break
        return None

    @property
    def pages(self):
        """
        Alias for self["pageCount"]
        """
        return self["pageCount"]

    @property
    def description(self):
        """
        Alias for self["description"]
        """
        return self["description"]

    @property
    def language(self):
        """
        Alias for self["language"]
        """
        return self["language"]

    @property
    def thumbnail_url(self):
        """
        Looks for the biggest thumbnail image URL to return.
        NOTE: To get bigger images out of Google, you have to do a request
        with the Google specific identifier.
        TODO: Strip weirdness out of URL
        """
        if not self["imageLinks"]:
            return None

        sizes = ("thumbnail", "smallThumbnail")
        for size in sizes:
            if size in self["imageLinks"]:
                return self["imageLinks"][size]
        return None

    def parse(self, data):
        """
        Parses out the relevant data from the raw data, and stores it for
        access as though this object were a dictionary.
        Modify this method for required vs. optional fields
        """

        if "volumeInfo" in data:
            item = data["volumeInfo"]
        else:
            raise GoogleBooksException("Expected to find volumeInfo, could not.")

        required = ("title",
                    "industryIdentifiers",)

        optional = ("authors",
                    "publisher",
                    "publishedDate",
                    "description",
                    "pageCount",
                    "imageLinks",
                    "language")

        book = { }

        for key in required:
            if key not in item:
                raise GoogleBooksException("Required key, %s, was not found", key)
            else:
                book[key] = item[key]

        for key in optional:
            if key in item:
                book[key] = item[key]
            else:
                book[key] = None

        return book

    def isbn_search(self, space, keys):
        """
        Performs a "priority search" on the search space, based on the
        order of search keys if they're in the search space.
        The expected type of the space is an iterable that contains
        dictionary-like objects, with the search keys. (In this case,
        Google Books industryIdentifiers list)
        The keys is an ordered tuple or list to search the dictionary for
        -- it returns the first key in the order it can find it.
        TODO: Make more generic
        """

        found = None    # Holds the currently found item
        index = None    # Holds the index of the key for current item

        for item in space:
            if item['type'] in keys:
                if item['type'] == keys[0]:
                    return item['identifier'] # If it's the first key, then return.
                else:
                    if index is None or keys.index(item['type']) < index:
                        found = item['identifier']
                        index = keys.index(item['type'])
                    else:
                        continue
            else:
                continue
        return found

    def serialize(self):
        """
        Returns a dictionary compatible to the Book model
        """
        return {
            'isbn':        self.isbn,
            'shortisbn':   self.shortisbn,
            'title':       self.title,
            'authors':     [a for a in self.authors],
            'publisher':   {'name':self.publisher, 'location':None},
            'pubdate':     self.pubdate,
            'pages':       self.pages,
            'description': self.description,
            'language':    self.language,
            'thumbnail':   self.thumbnail_url,
        }

    def __getitem__(self, name):
        """
        Provides read-only access to item dictionary, through normal
        dictionary access mechansim.
        """
        return self.item[name] if name in self else None

    def __contains__(self, name):
        return name in self.item

    def __str__(self):
        return "<BookDict: %s by %s>" % (self['title'], ', '.join(self['authors']))


if __name__ == "__main__":

    query = QueryBuilder(isbn="9781449356262")

    books = GoogleBooks()
    response = books.lookup(query)

    if response is None:
        print "Could not find query: %s" % query

    elif isinstance(response, list):
        for book in response:
            print book

    else:
        print response
        for k, v in response.serialize().items():
            print "%s: %s" % (k, v)
