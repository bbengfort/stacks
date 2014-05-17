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

from rest_framework import serializers
from rest_framework.compat import smart_text
from books.models import Book, Review, BookMedia

##########################################################################
## Serializers
##########################################################################

class BookSerializer(serializers.HyperlinkedModelSerializer):

    authors   = serializers.RelatedField(many=True)
    publisher = serializers.RelatedField(many=False)

    class Meta:
        model  = Book
        fields = ('url', 'title', 'pubdate', 'pages', 'description',
                  'cover', 'authors', 'publisher')

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model  = Review

class BookMediaSerializer(serializers.ModelSerializer):

    class Meta:
        model  = BookMedia
