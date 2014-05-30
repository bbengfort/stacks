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

import os
from .base import *

##########################################################################
## Production Settings
##########################################################################

## Debugging Settings
DEBUG            = environ_setting('DEBUG_DJANGO', False)
TEMPLATE_DEBUG   = False

## Hosts
ALLOWED_HOSTS    = ['stacks.bengfort.com',
                    'stacks-web-prod.elasticbeanstalk.com',
                    'localhost', '127.0.0.1']

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

## Static files in S3
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
