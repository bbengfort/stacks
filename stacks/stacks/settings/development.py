# stacks.settings.development
# Development environment specific settings
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Thu May 15 14:18:15 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: development.py [] benjamin@bengfort.com $

"""
Development environment specific settings
"""

##########################################################################
## Imports
##########################################################################

import os
from .base import *

##########################################################################
## Development Settings
##########################################################################

## Debugging Settings
DEBUG            = True
TEMPLATE_DEBUG   = True

## Hosts
ALLOWED_HOSTS    = ('127.0.0.1', 'localhost')

## Secret Key doesn't matter in Dev
SECRET_KEY = 'ag05z*%5)$+wccf@anpqe+u@7-^b#%=&9gezq64*ox2d#7v&&r'

## Content
MEDIA_ROOT       = os.path.join(PROJECT_DIR, 'media')

## Testing
#STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
#STATIC_URL          = 'https://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
