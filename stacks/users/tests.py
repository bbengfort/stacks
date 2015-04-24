# stacks.users.tests
# Unit Tests for the users app (and authentication)
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Wed May 28 10:02:54 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: tests.py [] benjamin@bengfort.com $

"""
Unit Tests for the users app (and authentication)
"""

##########################################################################
## Imports
##########################################################################

import hashlib

from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from users.models import Profile

##########################################################################
## User Fixture
##########################################################################

fixtures = {
    'user': {
        'username': 'jdoe',
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'jdoe@example.com',
        'password': 'supersecret',
    }
}

##########################################################################
## Model Tests
##########################################################################


class ProfileModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(**fixtures['user'])

    def test_profile_on_create(self):
        """
        Test the User post_save signal to create a profile
        """

        self.assertEqual(Profile.objects.count(), 1, "begin profile count mismatch (user mock has no profile?)")
        u = User.objects.create_user(username="test", email="test@example.com", password="password")
        self.assertEqual(Profile.objects.count(), 2, "additional profile object doesn't exist")
        self.assertIsNotNone(u.profile)

    def test_profile_email_hash_md5(self):
        """
        Ensure that the email_hash on a user is an MD5 digest
        """

        email   = "Jane.Doe@gmail.com"
        udigest = hashlib.md5(email).hexdigest()
        ldigest = hashlib.md5(email.lower()).hexdigest()

        u = User.objects.create_user(username="test", email=email, password="password")
        self.assertIsNotNone(u.profile, "user has no profile?")
        self.assertIsNotNone(u.profile.email_hash, "user has no email hash?")

        self.assertNotEqual(udigest, u.profile.email_hash, "email was not lower case before digest")
        self.assertEqual(ldigest, u.profile.email_hash, "email not hashed correctly")

    def test_profile_email_hash_create(self):
        """
        Email should be hashed on user create
        """

        digest = hashlib.md5(fixtures['user']['email']).hexdigest()

        self.assertIsNotNone(self.user.profile, "user has no profile?")
        self.assertIsNotNone(self.user.profile.email_hash, "user has no email hash?")
        self.assertEqual(digest, self.user.profile.email_hash, "email hash does not match expected")

    def test_profile_email_hash_update(self):
        """
        Email should be hashed on user update
        """

        newemail = "john.doe@gmail.com"
        digest   = hashlib.md5(newemail).hexdigest()

        self.user.email = newemail
        self.user.save()

        self.assertEqual(digest, self.user.profile.email_hash, "email hash does not match expected")

##########################################################################
## View Test Cases
##########################################################################


class MemberViewsTest(TestCase):
    """
    Test the various authenticated views of the app
    """

    fixtures = ['groups',]

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
            'app-root',
            'profile',
            #'book_detail',   # Requires title slug ...
            #'author_detail', # Requires author slug ...
        )

        msg = "View '%s' ('%s') responded to unauthenticated user."
        for name in protected:
            self.client.logout()  # Ensure we're logged out
            url = reverse(name)   # Get the url for this view
            social_auth = reverse('social:begin', args=('google-oauth2',))
            login_url = 'http://testserver%s/?next=%s' % (social_auth, url)

            response = self.client.get(url)
            self.assertEqual(response.status_code, 302, msg=msg % (name, url))
            self.assertEqual(response['Location'], login_url)

            # msg_prefix=msg % (name, url)
            # self.assertRedirects(response, login_url, msg_prefix=msg_prefix)


class UserViewsTest(TestCase):

    def setUp(self):
        self.user   = User.objects.create_user(**fixtures['user'])
        self.client = Client()

    def login(self):
        credentials = {
            'username': fixtures['user']['username'],
            'password': fixtures['user']['password'],
        }

        return self.client.login(**credentials)

    def logout(self):
        return self.client.logout();

    def test_profile_view_auth(self):
        """
        Assert that profile can only be viewed if logged in.
        """
        endpoint = reverse('profile')
        loginurl = reverse('social:begin', args=('google-oauth2',))
        params   = "next=%s" % endpoint
        expected = "%s/?%s" % (loginurl, params)
        response = self.client.get(endpoint)

        self.assertRedirects(response, expected, fetch_redirect_response=False)

    def test_profile_object(self):
        """
        Assert the profile gets the current user
        """

        endpoint = reverse('profile')

        self.login()
        response = self.client.get(endpoint)

        self.assertEqual(self.user, response.context['user'])

    def test_profile_template(self):
        """
        Check that the right template is being used
        """
        endpoint = reverse('profile')

        self.login()
        response = self.client.get(endpoint)

        self.assertTemplateUsed(response, 'registration/profile.html')

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
        endpoint = reverse('api:api-root')

        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, 403)
