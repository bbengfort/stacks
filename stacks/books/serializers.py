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
from stacks.utils.fields import AbsoluteFileField
from stacks.utils.fields import AbsoluteImageField
from stacks.utils.fields import MarkdownField

##########################################################################
## Serializers
##########################################################################


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializes an Author object for use in the API.
    """

    about      = MarkdownField()

    class Meta:
        model  = Author
        fields = ('id', 'name', 'about')


class PublisherSerializer(serializers.ModelSerializer):
    """
    Serializes the Publisher object for use in the API.
    """

    class Meta:
        model  = Publisher
        fields = ('id', 'name', 'location')


class BookMediaSerializer(serializers.ModelSerializer):
    """
    Serializes the BookMedia including file meta data and other important
    download data for a piece of media for a book.
    """

    book       = serializers.HyperlinkedRelatedField(view_name='api:book-detail', read_only=True)
    uploader   = serializers.HyperlinkedRelatedField(view_name='api:user-detail', read_only=True)
    content    = AbsoluteFileField()

    class Meta:
        model  = BookMedia
        fields = ('id','book', 'uploader', 'content', 'content_type', 'signature')


class SimpleBookMediaSerializer(BookMediaSerializer):
    """
    Serializes the BookMedia with a limited amount of meta data required
    only for nesting the serialization on the Book object.
    """

    class Meta:
        model  = BookMedia
        fields = ('id', 'content', 'content_type', 'signature')


class BookSerializer(serializers.ModelSerializer):
    """
    Complex, multi-relational Book object that includes the Author and
    Publisher serailization as well as any attached book media that is
    associated. This serializer also passes on download links (for covers
    and media) and provides the interface for POST data of books.
    """

    authors     = AuthorSerializer(many=True)
    publisher   = PublisherSerializer(many=False)
    media       = SimpleBookMediaSerializer(many=True)
    cover       = AbsoluteImageField()
    tags        = serializers.StringRelatedField(many=True)
    description = MarkdownField()

    class Meta:
        model   = Book
        fields  = ('id', 'title', 'slug', 'pubdate', 'pages', 'description',
                   'cover', 'authors', 'publisher', 'media', 'tags')


class ReviewSerializer(serializers.ModelSerializer):
    """
    Obligatory serializer for the Review object in the API.
    """

    review     = MarkdownField()

    class Meta:
        model  = Review
