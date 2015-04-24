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

##########################################################################
## Normal HTTP Views for Browser
##########################################################################


class BookList(MembershipRequired, ListView):

    model = Book


class BookDetail(MembershipRequired, DetailView):

    model = Book


class AuthorDetail(MembershipRequired, DetailView):

    model = Author
