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
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

from django.conf.global_settings import LANGUAGES

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
    language     = models.CharField( max_length=5, default="en", choices=LANGUAGES )
    pages        = models.PositiveSmallIntegerField( **nullable )
    description  = MarkupField( markup_type='markdown', **nullable )
    cover        = models.ImageField( max_length=255, upload_to=upload_path('covers', 'slug'), **nullable )
    publisher    = models.ForeignKey( "books.Publisher", related_name="books", null=True, blank=True, default=None )
    authors      = models.ManyToManyField( "books.Author", related_name="books" )
    critics      = models.ManyToManyField( "auth.User", through="books.Review", related_name="books")

    ## Taggit tags for extra meta ##
    tags         = TaggableManager()

    def uploaders(self):
        """
        Returns a distinct list of anyone that has uploaded media for this
        book or periodical, allowing validation of the owners of the media.
        """
        field_name = 'uploader'
        for item in self.media.distinct(field_name):
            yield getattr(item, field_name)

    @models.permalink
    def get_absolute_url(self):
        """
        Returns the Absolute URL (permalink) of the Book detail.
        """
        return ('books:book_detail', [self.slug])

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

    GENDER       = Choices(('M', 'Male'), ('F', 'Female'), ('O', 'Other'), ('?', 'Unknown'))

    name         = models.CharField( max_length=255 )
    slug         = AutoSlugField( populate_from='name', unique=True, editable=True, blank=True )
    headshot     = models.ImageField( max_length=255, upload_to=upload_path('authors', 'slug'), **nullable )
    about        = MarkupField( markup_type='markdown', **nullable )
    website      = models.URLField( **nullable )
    gender       = models.CharField( max_length=1, choices=GENDER, null=True, blank=True, default=None )
    born         = models.DateField( **nullable )
    died         = models.DateField( **nullable )
    genre        = models.TextField( **nullable )

    @models.permalink
    def get_absolute_url(self):
        """
        Returns the Absolute URL (permalink) of the Author detail.
        """
        return ('books:author_detail', [self.slug])

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
    content      = models.FileField( max_length=255, null=False, blank=False,
                                upload_to=upload_path('uploads', 'book__slug'))
    content_type = models.CharField( max_length=5, choices=TYPES )
    signature    = models.CharField( max_length=64, **nullable )

    def save(self, *args, **kwargs):
        self.signature = filehash(self.content)
        super(BookMedia, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s.%s" % (self.book.slug, self.content_type)

    class Meta:
        db_table = "book_media"
        verbose_name = "book media"
        verbose_name_plural = "book media"

## Ensure that data in s3 is cleaned up on delete
@receiver(pre_delete, sender=BookMedia)
def cleanup_content(sender, instance, **kwargs):
    if instance.content:
        # Must pass False to ensure FileField doesn't save the model.
        instance.content.delete(False)
