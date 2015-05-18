# books.views
# Views for the Book app including REST viewsets and HTML views.
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Fri May 16 23:56:12 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: views.py [] benjamin@bengfort.com $

"""
Views for the Book app including REST viewsets and HTML views.
"""

##########################################################################
## Imports
##########################################################################

from django.views.generic import ListView, DetailView

from rest_framework import viewsets

from books.models import *
from books.serializers import *
from users.mixins import MembershipRequired

##########################################################################
## API HTTP/JSON Views
##########################################################################


class AuthorViewSet(viewsets.ModelViewSet):

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class PublisherViewSet(viewsets.ModelViewSet):

    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer


class BookViewSet(viewsets.ModelViewSet):

    queryset = Book.objects.all()
    serializer_class = BookSerializer


class ReviewViewSet(viewsets.ModelViewSet):

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class BookMediaViewSet(viewsets.ModelViewSet):

    queryset = BookMedia.objects.all()
    serializer_class = BookMediaSerializer


from books.gbs import QueryBuilder, GoogleBooks
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

class GoogleBooksSearch(viewsets.ViewSet):

    def list(self, request):
        """
        The search endpoint - queries the Google Books API.
        """
        isbn   = request.query_params.get('isbn')
        title  = request.query_params.get('title')


        if isbn:
            # ISBN takes the highest preference
            query  = QueryBuilder(isbn=isbn)

        elif title:
            # Search for title keywords as second preference
            query  = QueryBuilder(intitle=title)

        else:
            # Required to search for either ISBN or Title
            return Response({
                "message": "Welcome to the Google Books Search interface, query with either title or isbn."
            })

        result = GoogleBooks(apikey=settings.GOOGLE_BOOKS_API_KEY).lookup(query)

        if result is None:
            return Response({
                'isbn': isbn,
                'success': False,
                'message': "Could not find an ISBN that matched the query."
            }, status=status.HTTP_404_NOT_FOUND)

        elif isinstance(result, list):
            return Response([
                book.serialize() for book in result
            ])

        else:
            return Response(result.serialize())

##########################################################################
## Normal HTTP Views for Browser
##########################################################################


class BookList(MembershipRequired, ListView):

    model = Book


class BookDetail(MembershipRequired, DetailView):

    model = Book


class AuthorDetail(MembershipRequired, DetailView):

    model = Author
