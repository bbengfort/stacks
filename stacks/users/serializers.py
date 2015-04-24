# users.serializers
# Serializers for the users and profile models
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Wed Apr 22 18:38:26 2015 -0400
#
# Copyright (C) 2015 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: serializers.py [] benjamin@bengfort.com $

"""
Serializers for the users and profile models
"""

##########################################################################
## Imports
##########################################################################

from users.models import Profile
from rest_framework import serializers
from django.contrib.auth.models import User

##########################################################################
## Serializers
##########################################################################


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializes the Profile object to embed into the User JSON
    """

    gravatar = serializers.CharField(read_only=True)
    location = serializers.StringRelatedField()

    class Meta:
        model  = Profile
        fields = ('biography', 'gravatar', 'location')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializes the User object for use in the API.
    """

    profile = ProfileSerializer(many=False, read_only=True)

    class Meta:
        model  = User
        fields = ('url', 'username', 'first_name', 'last_name', 'profile')
        extra_kwargs = {
            'url': {'view_name': 'api:user-detail', }
        }


class PasswordSerializer(serializers.Serializer):

    password = serializers.CharField(max_length=200)
    repeated = serializers.CharField(max_length=200)

    def validate(self, attrs):
        if attrs['password'] != attrs['repeated']:
            raise serializers.ValidationError("passwords do not match!")
        return attrs
