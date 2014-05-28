# stacks.urls
# The main URL router for the app
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Thu May 15 23:40:35 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: urls.py [] benjamin@bengfort.com $

"""
The main URL router for the app
"""

##########################################################################
## Imports
##########################################################################

from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from rest_framework import routers
from django.contrib import admin

from books.views import *
from member.views import *

##########################################################################
## Automatic Discovery of Endpoints
##########################################################################

## Admin
admin.autodiscover()

## API
router = routers.DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'authors', AuthorViewSet)
router.register(r'publishers', PublisherViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'media', BookMediaViewSet)
router.register(r'members', MemberViewSet)

##########################################################################
## The URL Patterns for the app
##########################################################################

urlpatterns = patterns('',
    # Admin URLs
    (r'^grappelli/', include('grappelli.urls')), # grappelli URLs
    url(r'^admin/', include(admin.site.urls)),   # Admin URLs

    # REST API Urls
    url(r'^api/', include(router.urls, namespace='api')),

    # Static Pages
    url(r'^$', BookList.as_view(template_name='site/index.html'), name='home'),
    url(r'^terms/$', TemplateView.as_view(template_name='site/legal/terms.html'), name='terms'),
    url(r'^privacy/$', TemplateView.as_view(template_name='site/legal/privacy.html'), name='privacy'),

    # Library Pages
    url(r'^library/', include('books.urls', namespace='books')),

    # Social Authentication URLs
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='auth_login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name='auth_logout'),
    url(r'^accounts/profile/$', ProfileView.as_view(), name='profile'),
)
