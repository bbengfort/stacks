# books.serializers
# Serializers for the REST Framework
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Fri May 16 23:50:53 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: serializers.py [] benjamin@bengfort.com $

"""
Serializers for the REST Framework
"""

##########################################################################
## Imports
##########################################################################

from books.models import *
from rest_framework import serializers
from rest_framework.compat import smart_text

##########################################################################
## Serializers
##########################################################################

class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializes an Author object for use in the API.
    """

    class Meta:
        model = Author

class PublisherSerializer(serializers.ModelSerializer):
    """
    Serializes the Publisher object for use in the API.
    """

    class Meta:
        model = Publisher

class BookSerializer(serializers.ModelSerializer):
    """
    Complex, multi-relational Book object that includes the Author and
    Publisher serailization as well as any attached book media that is
    associated. This serializer also passes on download links (for covers
    and media) and provides the interface for POST data of books.
    """

    authors   = serializers.RelatedField(many=True)
    publisher = serializers.RelatedField(many=False)

    class Meta:
        model  = Book
        fields = ('id', 'title', 'pubdate', 'pages', 'description',
                  'cover', 'authors', 'publisher')

class BookMediaSerializer(serializers.ModelSerializer):
    """
    Serializes the BookMedia including file meta data and other important
    download data for a piece of media for a book.
    """

    class Meta:
        model  = BookMedia

class ReviewSerializer(serializers.ModelSerializer):
    """
    Obligatory serializer for the Review object in the API.
    """

    class Meta:
        model  = Review

