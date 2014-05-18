# member.serializers
# Serializers for the members models
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Sun May 18 07:57:36 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: serializers.py [] benjamin@bengfort.com $

"""
Serializers for the members models
"""

##########################################################################
## Imports
##########################################################################

from member.models import *
from rest_framework import serializers
from rest_framework.compat import smart_text
from django.contrib.auth.models import User

##########################################################################
## Serializers
##########################################################################

class MemberSerializer(serializers.ModelSerializer):
    """
    Serializes the User object for use in the API.
    """

    class Meta:
        model  = User
        fields = ('id', 'username', 'first_name', 'last_name')
