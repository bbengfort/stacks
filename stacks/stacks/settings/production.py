# stacks.settings.production
# Production environment specific settings
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Wed Apr 22 14:34:54 2015 -0400
#
# Copyright (C) 2015 Bengfort.com
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

## Hosts
ALLOWED_HOSTS    = ['stacks.bengfort.com',
                    'stacks.herokuapp.com',
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

## Static files served by Nginx
STATIC_ROOT = '/var/www/stacks/static'
MEDIA_ROOT  = '/var/www/stacks/media'

## Email Settings
SERVER_EMAIL    = environ_setting("SERVER_EMAIL",
                                  "Stacks Admin <server@bengfort.com>")
EMAIL_USE_TLS   = True
EMAIL_HOST      = environ_setting("EMAIL_HOST", "smtp.gmail.com")
EMAIL_HOST_USER = environ_setting("EMAIl_HOST_USER", "server@bengfort.com")
EMAIL_HOST_PASSWORD = environ_setting("EMAIL_HOST_PASSWORD")
EMAIL_PORT      = 587
