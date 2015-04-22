# stacks.settings.development
# Development environment specific settings
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Wed Apr 22 14:33:43 2015 -0400
#
# Copyright (C) 2015 Bengfort.com
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

## Hosts
ALLOWED_HOSTS    = ('127.0.0.1', 'localhost')

## Content
MEDIA_ROOT       = os.path.join(PROJECT_DIR, 'media')
