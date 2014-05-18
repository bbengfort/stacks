# books.models
# Models for the Book library
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Fri May 16 20:23:31 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: models.py [] benjamin@bengfort.com $

"""
Models for the Book library
"""

##########################################################################
## Imports
##########################################################################

from django.db import models
from model_utils import Choices
from stacks.utils import nullable
from autoslug import AutoSlugField
from taggit.managers import TaggableManager
from stacks.utils import upload_path, filehash
from model_utils.models import TimeStampedModel
from markupfield.fields import MarkupField

##########################################################################
## Models for Book Information
##########################################################################

class Book(TimeStampedModel):
    """
    The Book model provides data access to a particular book in the stacks
    and is the primary relation for most other tables in the database. E.g.
    the book is the canonical representation of some literature.
    """

    isbn         = models.CharField( max_length=13, **nullable )
    title        = models.CharField( max_length=255 )
    slug         = AutoSlugField( populate_from='title', unique_with='pubdate__year' )
    pubdate      = models.DateField( **nullable )
    language     = models.CharField( max_length=5, default="en", null=True)
    pages        = models.PositiveSmallIntegerField( **nullable )
    description  = MarkupField( markup_type='markdown', **nullable )
    cover        = models.ImageField( max_length=255, upload_to=upload_path('covers', 'isbn'), **nullable )
    publisher    = models.ForeignKey( "books.Publisher", related_name="books" )
    authors      = models.ManyToManyField( "books.Author", related_name="books" )
    critics      = models.ManyToManyField( "auth.User", through="books.Review", related_name="books")

    ## Taggit tags for extra meta ##
    tags         = TaggableManager()

    def __unicode__(self):
        return "%s (%s)" % (self.title, self.pubdate.strftime('%Y'))

    class Meta:
        db_table = "books"
        ordering = ['-pubdate', '-created']
        get_latest_by = "modified"

class Publisher(TimeStampedModel):
    """
    Holds Publisher information for quick publishing lookups.
    """

    name         = models.CharField( max_length=255 )
    location     = models.CharField( max_length=255 )

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "publishers"
        ordering = ['-modified']
        get_latest_by = "modified"
        unique_together = ('name', 'location')

class Author(TimeStampedModel):
    """
    Holds Author information for quick author lookups.
    """

    name         = models.CharField( max_length=255 )
    about        = MarkupField( markup_type='markdown', **nullable )
    slug         = AutoSlugField( populate_from='name', unique=True, editable=True )

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "authors"
        ordering = ['-modified']
        get_latest_by = "modified"

##########################################################################
## Obligatory Review Model
##########################################################################

class Review(TimeStampedModel):
    """
    Connects users to books through reviews.
    """

    RATING       = Choices((0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'))

    user         = models.ForeignKey( 'auth.User', related_name='reviews' )
    book         = models.ForeignKey( 'books.Book', related_name='reviews' )
    rating       = models.PositiveSmallIntegerField( default=0, null=False, blank=True, choices=RATING )
    review       = MarkupField( markup_type='markdown', **nullable )
    date_read    = models.DateField( **nullable )

    class Meta:
        db_table = "reviews"
        ordering = ['-modified']
        get_latest_by = "modified"
        unique_together = ('user', 'book')

##########################################################################
## File Handling and Reference Model
##########################################################################

class BookMedia(TimeStampedModel):
    """
    Contains information about a stored file for a particular book.

    TODO: Compute the MD5 hash of the temporary upload on upload.
    """

    TYPES        = Choices(('pdf', 'PDF'), ('epub', 'ePub'), ('mobi', 'Mobi'),
                           ('aax', 'AAX'), ('apk', 'APK'), ('mp3', 'MP3'),)

    book         = models.ForeignKey( 'books.Book', related_name='media' )
    uploader     = models.ForeignKey( 'auth.User', related_name='uploads' )
    content      = models.FileField( max_length=255, upload_to='uploads' )
    content_type = models.CharField( max_length=5, choices=TYPES )
    signature    = models.CharField( max_length=64, **nullable )

    def save(self, *args, **kwargs):
        self.signature = filehash(self.content)
        super(BookMedia, self).save(*args, **kwargs)

    class Meta:
        db_table = "book_media"
        verbose_name = "book media"
        verbose_name_plural = "book media"
