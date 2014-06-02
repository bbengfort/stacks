# stacks.books.tests
# Tests for the books app in the Stacks project
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Wed May 28 10:14:45 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: tests.py [] benjamin@bengfort.com $

"""
Tests for the books app in the Stacks project
"""

##########################################################################
## Imports
##########################################################################

from .models import *
from unittest import skip
from django.test import TestCase
from django.contrib.auth.models import User
from stacks.utils import upload_path, ngetattr

##########################################################################
## Models Test Cases
##########################################################################

class BookModelTests(TestCase):
    """
    Test the methods on the Book Model
    """

    fixtures = ['initial_data.json']

    def test_cover_upload_to_path(self):
        """
        Assert that the upload_to path is correct for book covers

        This works by creating a book instance, then passing that directly
        to the upload_path function rather than trying to upload something
        completely. In the future we may want to try an actual upload.
        """

        # Set the expectations
        lookup        = {'isbn': 978143021936}
        expected_slug = u'the-definitive-guide-to-django'
        expected_path = u'covers/the-definitive-guide-to-django.png'

        # Fetch the book that we'll test
        book = Book.objects.get(**lookup)
        self.assertEqual(book.slug, expected_slug)

        # Grab the upload function and give it a file
        upload_to   = book._meta.get_field('cover').upload_to
        upload_path = upload_to(book, 'test_book_filename.png')
        self.assertEqual(upload_path, expected_path)

class AuthorModelTests(TestCase):
    """
    Test the methods on the Author Model
    """

    fixtures = ['initial_data.json']

    def test_headshot_upload_to_path(self):
        """
        Check that the upload_to path is correct for author headshots

        See the Book model test for more details.
        """

        # Set the expectations
        lookup        = {'pk': 1}
        expected_slug = u'dj-patil'
        expected_path = u'authors/dj-patil.jpg'

        # Fetch the author that we'll test
        author = Author.objects.get(**lookup)
        self.assertEqual(author.slug, expected_slug)

        # Grab the upload function and give it a file
        upload_to   = author._meta.get_field('headshot').upload_to
        upload_path = upload_to(author, 'apicture_of_a_person.jpg')
        self.assertEqual(upload_path, expected_path)

class BookMediaModelTests(TestCase):
    """
    Test the methods on the BookMedia model
    """

    fixtures = ['media.json']

    def test_content_required(self):
        """
        Assert that some content is required for this object
        """
        with self.assertRaisesRegexp(ValueError, "The 'content' attribute has no file associated with it."):
            media = BookMedia.objects.create(**{
                "book": Book.objects.all()[0],
                "uploader": User.objects.all()[0],
                "content_type": "epub",
            })

    @skip('not implemented')
    def test_signature(self):
        """
        Assert that the signature of the file isn't blank
        """
        pass

    @skip('not implemented')
    def test_media_remove_on_delete(self):
        """
        Ensure that media is removed from S3 on delete
        """
        pass

    def test_media_upload_to_path(self):
        """
        Check that the upload_to path is correct for media

        See Book model tests for more details.
        """
        # Set the expectations
        lookup        = {'pk': 1}
        expected_slug = u'the-definitive-guide-to-django'
        expected_path = u'uploads/the-definitive-guide-to-django.epub'

        # Fetch the media that we'll test
        media = BookMedia.objects.get(**lookup)
        self.assertEqual(media.book.slug, expected_slug)

        # Grab the upload function and give it a file
        upload_to   = media._meta.get_field('content').upload_to
        upload_path = upload_to(media, 'test_book_filename.epub')
        self.assertEqual(upload_path, expected_path)

##########################################################################
## Views Test Cases
##########################################################################

##########################################################################
## API Test Cases
##########################################################################

##########################################################################
## Utilities Test Cases
##########################################################################

class UtilityTestCase(TestCase):
    """
    Test various utilities related to the books app.
    """

    def test_ngetattr(self):
        """
        Test the multiple nested attribute lookup utility
        """

        class Thing(object):

            def __init__(self, **kwargs):
                for k,v in kwargs.items():
                    setattr(self,k,v)


        t1 = Thing(name='thing1', parent=None)
        t2 = Thing(name='thing2', parent=t1)
        t3 = Thing(name='thing3', parent=t2)
        t4 = Thing(name='thing4', parent=t3)

        self.assertEqual(ngetattr(t4, 'parent__parent__parent__name'), 'thing1')
        self.assertEqual(ngetattr(t4, 'parent__parent__name'), 'thing2')
        self.assertEqual(ngetattr(t4, 'parent__name'), 'thing3')
        self.assertEqual(ngetattr(t4, 'name'), 'thing4')
