# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import stacks.utils
import model_utils.fields
import autoslug.fields
import markupfield.fields
import django.utils.timezone
from django.conf import settings
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(unique=True, blank=True)),
                ('headshot', models.ImageField(default=None, max_length=255, null=True, upload_to=stacks.utils.PathUploader(b'authors', b'slug'), blank=True)),
                ('about', markupfield.fields.MarkupField(default=None, null=True, rendered_field=True, blank=True)),
                ('website', models.URLField(default=None, null=True, blank=True)),
                ('about_markup_type', models.CharField(default=b'markdown', max_length=30, editable=False, blank=True, choices=[(b'', b'--'), (b'html', 'HTML'), (b'plain', 'Plain'), (b'markdown', 'Markdown')])),
                ('_about_rendered', models.TextField(editable=False)),
                ('gender', models.CharField(default=None, max_length=1, null=True, blank=True, choices=[(b'M', b'Male'), (b'F', b'Female'), (b'O', b'Other'), (b'?', b'Unknown')])),
                ('born', models.DateField(default=None, null=True, blank=True)),
                ('died', models.DateField(default=None, null=True, blank=True)),
                ('genre', models.TextField(default=None, null=True, blank=True)),
            ],
            options={
                'ordering': ['-modified'],
                'db_table': 'authors',
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('isbn', models.CharField(default=None, max_length=13, null=True, blank=True)),
                ('title', models.CharField(max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(editable=False)),
                ('pubdate', models.DateField(default=None, null=True, blank=True)),
                ('language', models.CharField(default=b'en', max_length=5, choices=[(b'af', b'Afrikaans'), (b'ar', b'Arabic'), (b'ast', b'Asturian'), (b'az', b'Azerbaijani'), (b'bg', b'Bulgarian'), (b'be', b'Belarusian'), (b'bn', b'Bengali'), (b'br', b'Breton'), (b'bs', b'Bosnian'), (b'ca', b'Catalan'), (b'cs', b'Czech'), (b'cy', b'Welsh'), (b'da', b'Danish'), (b'de', b'German'), (b'el', b'Greek'), (b'en', b'English'), (b'en-au', b'Australian English'), (b'en-gb', b'British English'), (b'eo', b'Esperanto'), (b'es', b'Spanish'), (b'es-ar', b'Argentinian Spanish'), (b'es-mx', b'Mexican Spanish'), (b'es-ni', b'Nicaraguan Spanish'), (b'es-ve', b'Venezuelan Spanish'), (b'et', b'Estonian'), (b'eu', b'Basque'), (b'fa', b'Persian'), (b'fi', b'Finnish'), (b'fr', b'French'), (b'fy', b'Frisian'), (b'ga', b'Irish'), (b'gl', b'Galician'), (b'he', b'Hebrew'), (b'hi', b'Hindi'), (b'hr', b'Croatian'), (b'hu', b'Hungarian'), (b'ia', b'Interlingua'), (b'id', b'Indonesian'), (b'io', b'Ido'), (b'is', b'Icelandic'), (b'it', b'Italian'), (b'ja', b'Japanese'), (b'ka', b'Georgian'), (b'kk', b'Kazakh'), (b'km', b'Khmer'), (b'kn', b'Kannada'), (b'ko', b'Korean'), (b'lb', b'Luxembourgish'), (b'lt', b'Lithuanian'), (b'lv', b'Latvian'), (b'mk', b'Macedonian'), (b'ml', b'Malayalam'), (b'mn', b'Mongolian'), (b'mr', b'Marathi'), (b'my', b'Burmese'), (b'nb', b'Norwegian Bokmal'), (b'ne', b'Nepali'), (b'nl', b'Dutch'), (b'nn', b'Norwegian Nynorsk'), (b'os', b'Ossetic'), (b'pa', b'Punjabi'), (b'pl', b'Polish'), (b'pt', b'Portuguese'), (b'pt-br', b'Brazilian Portuguese'), (b'ro', b'Romanian'), (b'ru', b'Russian'), (b'sk', b'Slovak'), (b'sl', b'Slovenian'), (b'sq', b'Albanian'), (b'sr', b'Serbian'), (b'sr-latn', b'Serbian Latin'), (b'sv', b'Swedish'), (b'sw', b'Swahili'), (b'ta', b'Tamil'), (b'te', b'Telugu'), (b'th', b'Thai'), (b'tr', b'Turkish'), (b'tt', b'Tatar'), (b'udm', b'Udmurt'), (b'uk', b'Ukrainian'), (b'ur', b'Urdu'), (b'vi', b'Vietnamese'), (b'zh-cn', b'Simplified Chinese'), (b'zh-hans', b'Simplified Chinese'), (b'zh-hant', b'Traditional Chinese'), (b'zh-tw', b'Traditional Chinese')])),
                ('pages', models.PositiveSmallIntegerField(default=None, null=True, blank=True)),
                ('description', markupfield.fields.MarkupField(default=None, null=True, rendered_field=True, blank=True)),
                ('cover', models.ImageField(default=None, max_length=255, null=True, upload_to=stacks.utils.PathUploader(b'covers', b'slug'), blank=True)),
                ('description_markup_type', models.CharField(default=b'markdown', max_length=30, editable=False, blank=True, choices=[(b'', b'--'), (b'html', 'HTML'), (b'plain', 'Plain'), (b'markdown', 'Markdown')])),
                ('_description_rendered', models.TextField(editable=False)),
                ('authors', models.ManyToManyField(related_name='books', to='books.Author')),
            ],
            options={
                'ordering': ['-pubdate', '-created'],
                'db_table': 'books',
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='BookMedia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('content', models.FileField(max_length=255, upload_to=stacks.utils.PathUploader(b'uploads', b'book__slug'))),
                ('content_type', models.CharField(max_length=5, choices=[(b'pdf', b'PDF'), (b'epub', b'ePub'), (b'mobi', b'Mobi'), (b'aax', b'AAX'), (b'apk', b'APK'), (b'mp3', b'MP3')])),
                ('signature', models.CharField(default=None, max_length=64, null=True, blank=True)),
                ('book', models.ForeignKey(related_name='media', to='books.Book')),
                ('uploader', models.ForeignKey(related_name='uploads', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'book_media',
                'verbose_name': 'book media',
                'verbose_name_plural': 'book media',
            },
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['-modified'],
                'db_table': 'publishers',
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('rating', models.PositiveSmallIntegerField(default=0, blank=True, choices=[(0, b'0'), (1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'5')])),
                ('review', markupfield.fields.MarkupField(default=None, null=True, rendered_field=True, blank=True)),
                ('review_markup_type', models.CharField(default=b'markdown', max_length=30, editable=False, blank=True, choices=[(b'', b'--'), (b'html', 'HTML'), (b'plain', 'Plain'), (b'markdown', 'Markdown')])),
                ('date_read', models.DateField(default=None, null=True, blank=True)),
                ('_review_rendered', models.TextField(editable=False)),
                ('book', models.ForeignKey(related_name='reviews', to='books.Book')),
                ('user', models.ForeignKey(related_name='reviews', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-modified'],
                'db_table': 'reviews',
                'get_latest_by': 'modified',
            },
        ),
        migrations.AlterUniqueTogether(
            name='publisher',
            unique_together=set([('name', 'location')]),
        ),
        migrations.AddField(
            model_name='book',
            name='critics',
            field=models.ManyToManyField(related_name='books', through='books.Review', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.ForeignKey(related_name='books', default=None, blank=True, to='books.Publisher', null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together=set([('user', 'book')]),
        ),
    ]
