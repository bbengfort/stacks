# stacks.utils.fields
# Custom fields for Models and Serializers
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Sun May 18 09:14:24 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: fields.py [] benjamin@bengfort.com $

"""
Custom fields for Models and Serializers
"""

##########################################################################
## Imports
##########################################################################

from rest_framework import serializers
from django.templatetags.static import static

##########################################################################
## Custom Serializer Fields
##########################################################################


class AbsoluteFileField(serializers.FileField):

    def to_native(self, value):
        request = self.context.get('request', None)
        if request:
            if value:
                return request.build_absolute_uri(value.url)
            return None
        return value.url


class AbsoluteImageField(serializers.ImageField):

    def to_native(self, value):
        request = self.context.get('request', None)
        if request:
            if value:
                return request.build_absolute_uri(value.url)

            # TODO: Put the nocover URL into settings
            return static('img/nocover.jpg')
        return value.url

##########################################################################
## Markdown Field
##########################################################################


class MarkdownField(serializers.WritableField):

    def to_native(self, obj):
        return unicode(obj)
