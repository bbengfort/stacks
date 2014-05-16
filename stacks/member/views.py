# member.views
# Views for member and contributor management
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Fri May 16 15:38:56 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: views.py [] benjamin@bengfort.com $

"""
Views for member and contributor management
"""

##########################################################################
## Imports
##########################################################################

import urllib
import hashlib


from .mixins import LoginRequired
from django.views.generic import TemplateView

##########################################################################
## Views
##########################################################################

class ProfileView(LoginRequired, TemplateView):
    """
    A simple template view to display a reviewer's profile including their
    upvoting and down voting statistics.
    """

    template_name = "registration/profile.html"

    def get_gravatar_url(self, email, size=200, default="mm"):
        """
        Computes the gravatar url from an email address
        """
        digest = hashlib.md5(email.lower()).hexdigest()
        params = urllib.urlencode({'d': default, 's': str(size)})
        grvurl = "http://www.gravatar.com/avatar/%s?%s" % (digest, params)
        return grvurl

    def get_context_data(self, **kwargs):
        """
        Computes the gravatar from the user email and adds data to the
        context to render the template.
        """
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['profile']  = self.request.user
        context['gravatar'] = self.get_gravatar_url(self.request.user.email)
        return context
