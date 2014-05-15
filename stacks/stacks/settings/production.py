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
