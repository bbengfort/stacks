# stacks.settings.production
# Production environment specific settings
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Thu May 15 14:17:57 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: production.py [] benjamin@bengfort.com $

"""
Production environment specific settings
"""

##########################################################################
## Imports
##########################################################################

from .base import *

##########################################################################
## Production Settings
##########################################################################

## Debugging Settings
DEBUG            = False
TEMPLATE_DEBUG   = False

## Hosts
ALLOWED_HOSTS    = ['stacks.bengfort.com',]

## Content
STATIC_ROOT      = "/var/www/stacks/static/"
MEDIA_ROOT       = "/var/www/stacks/media/"

## Database Settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': environ_setting('RDS_DB_NAME'),
        'USER': environ_setting('RDS_USERNAME'),
        'PASSWORD': environ_setting('RDS_PASSWORD'),
        'HOST': environ_setting('RDS_HOSTNAME'),
        'PORT': environ_setting('RDS_PORT'),
    }
}
