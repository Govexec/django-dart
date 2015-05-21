# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Custom_Ad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=255)),
                ('slug', models.CharField(max_length=255)),
                ('type', models.IntegerField(default=0, choices=[(0, b'Custom HTML'), (1, b'Image/URL')])),
                ('url', models.URLField(help_text=b'Click tag URL', null=True, blank=True)),
                ('image', models.ImageField(help_text=b'Image for custom ad', null=True, upload_to=b'img/upload/custom_ads', blank=True)),
                ('embed', ckeditor.fields.RichTextField(null=True, blank=True)),
                ('text_version', models.TextField(help_text=b'Text version of ad for newsletters or Javascript disabled browsers', blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Custom Ad',
                'verbose_name_plural': 'Custom Ads',
            },
        ),
        migrations.CreateModel(
            name='Custom_Ad_Template',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=255)),
                ('template', ckeditor.fields.RichTextField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Custom Ad Template',
                'verbose_name_plural': 'Custom Ad Templates',
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.CharField(help_text=b'This will be the same field passed to DART as the position', max_length=255)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Ad Positions',
            },
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.CharField(help_text=b'This is the same field passed to DART as the site', max_length=255, verbose_name=b'DART site handle')),
                ('slug_dev', models.CharField(help_text=b'Development DART site handle to be used when DEBUG is enabled', max_length=255, verbose_name=b'DART development site handle', blank=True)),
                ('disable_ad_manager', models.BooleanField(default=True, help_text=b'Toggles whether this app controls display of ad positions and allow custom HTML to be inserted')),
                ('default_render_format', models.PositiveIntegerField(default=0, help_text=b'Default type of DART code to render if not specified in ad tag', choices=[(0, b'Javascript'), (1, b'Blank'), (2, b'Iframe')])),
                ('network_code', models.CharField(default=b'', help_text=b'DART network code if needed', max_length=100, blank=True)),
                ('default_zone', models.CharField(default=b'', help_text=b"DART handle to use for pages that don't specify a zone", max_length=100, blank=True)),
                ('site', models.ForeignKey(to='sites.Site')),
            ],
            options={
                'verbose_name': 'Site',
                'verbose_name_plural': 'Sites',
                'permissions': (('add_site', 'Can add site'), ('change_site', 'Can change site'), ('delete_site', 'Can delete site')),
            },
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('width', models.PositiveSmallIntegerField(default=0, help_text=b'Use zero for unknown/variable values', blank=True)),
                ('height', models.PositiveSmallIntegerField(default=0, help_text=b'Use zero for unknown/variable values', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.CharField(help_text=b'This will be the same field passed to DART as the zone', max_length=255)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'Ad Zones',
            },
        ),
        migrations.CreateModel(
            name='Zone_Position',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enabled', models.IntegerField(default=1, choices=[(0, b'Disabled'), (1, b'Enabled'), (2, b'Scheduled')])),
                ('sync', models.BooleanField(default=True, help_text=b'Determines whether the position is synced with DART when sync task is run.  Otherwise enabled manually.')),
                ('date_published', models.DateTimeField(blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('custom_ad', models.ForeignKey(blank=True, to='dart.Custom_Ad', null=True)),
                ('position', models.ForeignKey(to='dart.Position')),
                ('zone', models.ForeignKey(to='dart.Zone')),
            ],
            options={
                'ordering': ['zone__name'],
                'verbose_name': 'Enabled Position',
                'verbose_name_plural': 'Enabled Positions',
            },
        ),
        migrations.AddField(
            model_name='zone',
            name='position',
            field=models.ManyToManyField(to='dart.Position', through='dart.Zone_Position'),
        ),
        migrations.AddField(
            model_name='zone',
            name='site',
            field=models.ManyToManyField(to='dart.Site', blank=True),
        ),
        migrations.AddField(
            model_name='position',
            name='sizes',
            field=models.ManyToManyField(to='dart.Size'),
        ),
        migrations.AddField(
            model_name='custom_ad',
            name='load_template',
            field=models.ForeignKey(default=None, blank=True, to='dart.Custom_Ad_Template', help_text=b'Load HTML code into the embed field from a pre-defined template', null=True),
        ),
    ]
