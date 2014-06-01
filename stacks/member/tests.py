# stacks.member.tests
# Unit Tests for the Member app (and authentication)
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Wed May 28 10:02:54 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: tests.py [] benjamin@bengfort.com $

"""
Unit Tests for the Member app (and authentication)
"""

##########################################################################
## Imports
##########################################################################

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group

##########################################################################
## View Test Cases
##########################################################################

class MemberViewsTest(TestCase):
    """
    Test the various authenticated views of the app
    """

    def test_splash_page_redirect_non_members(self):
        """
        Ensure authenticated non-members are redirected to their profile
        """
        self.test_user = User.objects.create_user('tester', password='secret')
        self.client.login(username='tester', password='secret')
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, reverse('profile'))

    def test_splash_page_redirect_members(self):
        """
        Ensure authenticated members are redirected to the app
        """
        self.test_user = User.objects.create_user('tester', password='secret')
        self.test_user.groups.add(Group.objects.get(name='Member'))
        self.client.login(username='tester', password='secret')
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, reverse('app-root'))

    def test_splash_page(self):
        """
        Ensure unauthenticated users are not redirected
        """
        self.client.logout()
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'site/index.html')

    def test_app_login_required(self):
        """
        Assert that access to any view in the app requires login
        """

        # List of views that should be protected
        protected = (
            #'home', # TODO!
            'profile',
            #'book_detail',   # Requires title slug ...
            #'author_detail', # Requires author slug ...
        )

        msg = "View '%s' ('%s') responded to unauthenticated user."
        for name in protected:
            self.client.logout()  # Ensure we're logged out
            url = reverse(name)   # Get the url for this view
            login_url = reverse('auth_login') + '?next=' + url
            response = self.client.get(url)
            self.assertRedirects(response, login_url, msg_prefix=msg % (name, url))

##########################################################################
## API Test Cases
##########################################################################

class MemberAPITestCase(TestCase):
    """
    Test the various API views that manage Members
    """

    def test_member_api_auth_required(self):
        """
        Test that API access is Login-Only
        """
        self.client.logout()
        endpoint = reverse('api-root')
