# stacks.utils
# Utilities for the entire Stacks project
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Wed Apr 22 18:32:13 2015 -0400
#
# Copyright (C) 2015 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: __init__.py [] benjamin@bengfort.com $

"""
Utilities for the entire Stacks project
"""

##########################################################################
## Imports
##########################################################################

import os
import hashlib

from django.utils.deconstruct import deconstructible

##########################################################################
## Utilities
##########################################################################

## Nullable kwargs for models
nullable = {'blank': True, 'null': True, 'default': None}

##########################################################################
## Helper functions
##########################################################################


def ngetattr(thing, field, default=None):
    """
    Performs multiple nested object lookup by spliting on the Django style
    '__' accessor and coninually accessing nested objects until done.
    """
    field = field.split('__')
    for f in field:
        thing = getattr(thing, f, default)
    return thing


def filehash(fp, algorithm='sha1'):
    """
    Returns the hexdigest of the hash of the contents of a file with the
    particular algorithm specified as the argument to the function.
    """
    stream = getattr(hashlib, algorithm)()
    for chunk in fp.chunks():
        stream.update(chunk)
    return stream.hexdigest()


##########################################################################
## Callable dynamic classes
##########################################################################


@deconstructible
class PathUploader(object):

    def __init__(self, path, field='slug'):
        """
        Object callable that computes the upload_path based on the field of a
        model. This class is used instead of a function wrapper to support
        (hopefully) migrations.
        """

        self.path  = path
        self.field = field

    def __eq__(self, other):
        """
        Equality is used in migrations to ensure that things haven't changed.
        """
        return (
            self.path == other.path and
            self.field == other.field
        )

    def __call__(self, instance, filename):
        base, ext  = os.path.splitext(filename)
        name = ngetattr(instance, self.field, None)

        if not name:
            name = base

        name += ext
        return os.path.join(self.path, name)
