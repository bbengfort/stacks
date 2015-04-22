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


def upload_path(path, field='slug'):
    """
    Computes the upload_path based on the field of a model.
    """
    def wrapper(instance, filename):
        base, ext  = os.path.splitext(filename)
        name = ngetattr(instance, field, None)

        if not name:
            name = base

        name += ext
        return os.path.join(path, name)
    return wrapper


def filehash(fp, algorithm='sha1'):
    """
    Returns the hexdigest of the hash of the contents of a file with the
    particular algorithm specified as the argument to the function.
    """
    stream = getattr(hashlib, algorithm)()
    for chunk in fp.chunks():
        stream.update(chunk)
    return stream.hexdigest()
