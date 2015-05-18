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

    class Meta:
        model  = Profile
        fields = ('biography', 'gravatar', 'location')
        read_only_fields = ('gravatar',)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializes the User object for use in the API.
    """

    profile = ProfileSerializer(many=False, read_only=False)

    class Meta:
        model  = User
        fields = ('url', 'username', 'first_name', 'last_name', 'email', 'profile')
        read_only_fields = ('username',)
        extra_kwargs = {
            'url': {'view_name': 'api:user-detail', }
        }

    def update(self, instance, validated_data):
        """
        To support nested update on the Profile, we include this method to
        automatically update the nested relation. Note that `create` is not
        implemented, so the API cannot automatically create a profile (yet).
        """
        print validated_data
        profile = validated_data.pop('profile')
        print profile.items()


        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        for attr, value in profile.items():
            setattr(instance.profile, attr, value)


        instance.profile.save()
        instance.save()
        return instance


class PasswordSerializer(serializers.Serializer):

    password = serializers.CharField(max_length=200)
    repeated = serializers.CharField(max_length=200)

    def validate(self, attrs):
        if attrs['password'] != attrs['repeated']:
            raise serializers.ValidationError("passwords do not match!")
        return attrs
