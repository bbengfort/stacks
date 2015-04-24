# stacks.wsgi
# WSGI config for stacks project.
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Wed Apr 22 17:54:47 2015 -0400
#
# Copyright (C) 2015 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: wsgi.py [] benjamin@bengfort.com $

"""
WSGI config for stacks project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

##########################################################################
## Imports
##########################################################################

import os

from django.core.wsgi import get_wsgi_application

##########################################################################
## WSGI Configuration
##########################################################################

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stacks.settings")

application = get_wsgi_application()
