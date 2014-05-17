# books.admin
# Registration of books models to the admin
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Fri May 16 22:57:22 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: admin.py [] benjamin@bengfort.com $

"""
Registration of books models to the admin
"""

##########################################################################
## Imports
##########################################################################

from books.models import *
from django.contrib import admin

##########################################################################
## Register your models here.
##########################################################################

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Review)
admin.site.register(BookMedia)
