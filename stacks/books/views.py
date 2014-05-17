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

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from member.mixins import LoginRequired
from books.models import *
from books.serializers import *
from django.contrib.auth.models import *

##########################################################################
## API HTTP/JSON Views
##########################################################################

class BookViewSet(viewsets.ModelViewSet):

    queryset = Book.objects.all()
    serializer_class = BookSerializer

class ReviewViewSet(viewsets.ModelViewSet):

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class BookMediaViewSet(viewsets.ModelViewSet):

    queryset = BookMedia.objects.all()
    serializer_class = BookMediaSerializer
