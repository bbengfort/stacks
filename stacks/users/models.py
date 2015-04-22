# users.models
# Contains additional User profile data but no authentication
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Wed Apr 22 18:28:52 2015 -0400
#
# Copyright (C) 2015 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: models.py [] benjamin@bengfort.com $

"""
Contains additional User profile data but no authentication
"""

##########################################################################
## Imports
##########################################################################

import urllib
import hashlib

from django.db import models
from stacks.utils import nullable
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse

##########################################################################
## Module Constants
##########################################################################

BASE_GRAVATAR_URL = "http://www.gravatar.com/avatar/%s?%s"

##########################################################################
## UserProfile model
##########################################################################


class Profile(models.Model):

    user       = models.OneToOneField(User, editable=False)
    email_hash = models.CharField(max_length=32, editable=False)
    biography  = models.CharField(max_length=255, **nullable)
    location   = models.CharField(max_length=255, **nullable)

    def get_gravatar_url(self, size=200, default="mm"):
        """
        Computes the gravatar url from an email address
        """
        params = urllib.urlencode({'d': default, 's': str(size)})
        grvurl = BASE_GRAVATAR_URL % (self.email_hash, params)
        return grvurl

    @property
    def gravatar(self):
        return self.get_gravatar_url()

    @property
    def gravatar_icon(self):
        return self.get_gravatar_url(size=24)

    @property
    def full_name(self):
        return self.user.get_full_name()

    @property
    def full_email(self):
        email = "%s <%s>" % (self.full_name, self.user.email)
        return email.strip()

    def get_api_detail_url(self):
        """
        Returns the API detail endpoint for the object
        """
        return reverse('api:user-detail', args=(self.pk,))

    def __unicode__(self):
        return self.full_email

##########################################################################
## Signals
##########################################################################


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    """
    Creates a Profile object for the user if it doesn't exist, or updates
    it with new information from the User (e.g. the gravatar).
    """
    ## Compute the email hash
    digest = hashlib.md5(instance.email.lower()).hexdigest()

    if created:
        Profile.objects.create(user=instance, email_hash=digest)
    else:
        instance.profile.email_hash = digest
        instance.profile.save()
