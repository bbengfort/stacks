# utils
# Helper code for the Stacks package
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Fri May 16 20:31:56 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: __init__.py [] benjamin@bengfort.com $

"""
Helper code for the Stacks package
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
nullable = { 'blank': True, 'null': True, 'default':None }

def upload_path(path, field='slug'):
    def wrapper(instance, filename):
        base, ext  = os.path.splitext(filename)
        name = getattr(instance, field, None)

        if not name:
            name = base

        name += ext
        return os.path.join(path, name)
    return wrapper

def filehash(fp, algorithm='sha1'):
    stream = getattr(hashlib, algorithm)()
    for chunk in fp.chunks():
        stream.update(chunk)
    return stream.hexdigest()