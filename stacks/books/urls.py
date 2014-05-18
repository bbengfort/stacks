# books.urls
# Router for the Books display pages.
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Sun May 18 13:26:03 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: urls.py [] benjamin@bengfort.com $

"""
Router for the Books display pages.
"""

##########################################################################
## Imports
##########################################################################

from books.views import *
from django.conf.urls import patterns, include, url

##########################################################################
## URL Patterns
##########################################################################

urlpatterns = patterns('',
    url(r'^books/(?P<slug>[-\w]+)/$', BookDetail.as_view(), name='book_detail'),
    url(r'^authors/(?P<slug>[-\w]+)/$', AuthorDetail.as_view(), name='author_detail'),
)
