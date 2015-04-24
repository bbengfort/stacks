# stacks.views
# Views for the project and application that don't require models
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Wed Apr 22 19:59:23 2015 -0400
#
# Copyright (C) 2015 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: views.py [] benjamin@bengfort.com $

"""
Views for the project and application that don't require models
"""

##########################################################################
## Imports
##########################################################################

import stacks

from datetime import datetime
from django.shortcuts import redirect
from users.mixins import MembershipRequired, is_member
from django.views.generic import TemplateView

from rest_framework import viewsets
from rest_framework.response import Response

##########################################################################
## Application Views
##########################################################################


class SplashPage(TemplateView):
    """
    Main splash page for the app. Although this is essentially a simple
    webpage with no need for extra context, this view does check if the
    user is logged in, and if so, immediately redirects them to the app.
    """

    template_name = "site/index.html"

    def dispatch(self, request, *args, **kwargs):
        """
        If a user is authenticated, redirect to the Application, otherwise
        serve normal template view as expected.
        """
        if request.user.is_authenticated():
            if is_member(request.user):
                return redirect('app-root', permanent=False)
            return redirect('profile', permanent=False)
        return super(SplashPage, self).dispatch(request, *args, **kwargs)


class WebAppView(MembershipRequired, TemplateView):
    """
    Authenticated web application view that serves all context and content
    to kick off the Backbone front-end application.
    """

    template_name = "app/index.html"


##########################################################################
## API Views for this application
##########################################################################


class HeartbeatViewSet(viewsets.ViewSet):
    """
    Endpoint for heartbeat checking, including the status and version.
    """

    def list(self, request):
        return Response({
            "status": "ok",
            "version": stacks.get_version(),
            "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        })
