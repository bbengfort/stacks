# stacks.urls
# The main URL router for the project
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Wed Apr 22 14:31:48 2015 -0400
#
# Copyright (C) 2015 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: urls.py [] benjamin@bengfort.com $

"""
The main URL router for the project
"""

#############################################################################
## Imports
#############################################################################

from django.conf.urls import include, url
from django.contrib import admin

from django.views.generic import TemplateView

#############################################################################
## The URL Patterns for the app
#############################################################################

urlpatterns = [
    ## Admin URLs
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),

    ## Site Pages
    url(r'^$', TemplateView.as_view(template_name='site/index.html'), name='home'),
    url(r'^terms/$', TemplateView.as_view(template_name='site/legal/terms.html'), name='terms'),
    url(r'^privacy/$', TemplateView.as_view(template_name='site/legal/privacy.html'), name='privacy'),

    ## Membership URLs
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    # url(r'^profile/$', ProfileView.as_view(), name='profile'),
]
