# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management import call_command
from django.db import migrations

fixture = 'groups'


def load_fixture(apps, schema_editor):
    """
    Call the django management comamnd for loading the Member fixture
    """
    call_command('loaddata', fixture, app_label='users')


def unload_fixture(apps, schema_editor):
    """
    Brutally delete all entries for the model
    """
    Group = apps.get_model('auth', 'Group')
    Group.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_fixture, reverse_code=unload_fixture),
    ]
