# stacks.settings.base
# Default Django settings for entire Memorandi project
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Thu May 15 14:15:14 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: base.py [] benjamin@bengfort.com $

"""
Django settings for stacks project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

##########################################################################
## Imports
##########################################################################

import os

##########################################################################
## Helper function for environmental settings
##########################################################################

def environ_setting(name, default=None):
    """
    Fetch setting from the environment- if not found, then this setting is
    ImproperlyConfigured.
    """
    if name not in os.environ and default is None:
        from django.core.exceptions import ImproperlyConfigured
        raise ImproperlyConfigured(
            "The {0} ENVVAR is not set.".format(name)
        )

    return os.environ.get(name, default)

##########################################################################
## Build Paths inside of project with os.path.join
##########################################################################

BASE_DIR    = os.path.dirname(os.path.dirname(__file__))
PROJECT_DIR = os.path.normpath(os.path.join(BASE_DIR, os.pardir))

##########################################################################
## Secret settings - do not store!
##########################################################################

SECRET_KEY = environ_setting("SECRET_KEY")

##########################################################################
## Database Settings
##########################################################################

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': environ_setting('DB_NAME', 'stacks'),
        'USER': environ_setting('DB_USER', 'django'),
        'PASSWORD': environ_setting('DB_PASS', ''),
        'HOST': environ_setting('DB_HOST', 'localhost'),
        'PORT': environ_setting('DB_PORT', '5432'),
    },
}

##########################################################################
## Runtime settings
##########################################################################

## Debugging Settings
DEBUG            = False
TEMPLATE_DEBUG   = False

## Hosts
ALLOWED_HOSTS    = []

## WSGI Configuration
ROOT_URLCONF     = 'stacks.urls'
WSGI_APPLICATION = 'stacks.wsgi.application'

## Application Definition
INSTALLED_APPS   = (
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party apps
    'taggit',
    'social.apps.django_app.default',
    'rest_framework',

    # Stacks Apps
    'books',
    'member',
)

## Request Handling
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

## Localization
LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'America/New_York'
USE_I18N      = True
USE_L10N      = True
USE_TZ        = True

##########################################################################
## Content (Static, Media, Templates)
##########################################################################

## Static Files
STATIC_URL          =  '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATICFILES_DIRS    = (
    os.path.join(PROJECT_DIR, 'static'),
)

## Template Files.
TEMPLATE_DIRS       = (
    os.path.join(PROJECT_DIR, 'templates'),
)

## Uploaded Media
MEDIA_URL           = "/media/"

## Additional template context
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "social.apps.django_app.context_processors.backends",
    "social.apps.django_app.context_processors.login_redirect",
)

## Set default file storage handler to hash the names
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

##########################################################################
## Logging and Error Reporting
##########################################################################

ADMINS          = (
    ('Benjamin Bengfort', 'benjamin@bengfort.com'),
)

SERVER_EMAIL    = 'Dakota <server@bengfort.com>'
EMAIL_USE_TLS   = True
EMAIL_HOST      = 'smtp.gmail.com'
EMAIL_HOST_USER = 'server@bengfort.com'
EMAIL_HOST_PASSWORD = environ_setting("EMAIL_HOST_PASSWORD")
EMAIL_PORT      = 587

##########################################################################
## Social Authentication
##########################################################################

## Support for Social Auth authentication backends
AUTHENTICATION_BACKENDS = (
    'social.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

## Social authentication strategy
SOCIAL_AUTH_STRATEGY = 'social.strategies.django_strategy.DjangoStrategy'
SOCIAL_AUTH_STORAGE = 'social.apps.django_app.default.models.DjangoStorage'

## Google-specific authentication keys
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = environ_setting("GOOGLE_OAUTH2_CLIENT_ID", "")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = environ_setting("GOOGLE_OAUTH2_CLIENT_SECRET", "")

## Login URLs and Redirects
LOGIN_URL  = 'auth_login'
LOGOUT_URL = 'auth_logout'
LOGIN_REDIRECT_URL = "/"

##########################################################################
## Grappelli Configuration
##########################################################################

GRAPPELLI_ADMIN_TITLE = "Bengfort Stacks Admin"

##########################################################################
## REST Framework
##########################################################################

REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),

    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
    'rest_framework.serializers.ModelSerializer',

    # Use Django's standard `django.contrib.auth` permissions
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],

    'PAGINATE_BY': 50,
}

##########################################################################
## AWS Access Keys
##########################################################################

AWS_ACCESS_KEY_ID       = environ_setting('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY   = environ_setting('AWS_SECRET_KEY', '')
AWS_STORAGE_BUCKET_NAME = environ_setting('AWS_EB_BUCKET', 'bengfortstacks')
#AWS_CALLING_FORMAT      = CallingFormat.SUBDOMAIN
