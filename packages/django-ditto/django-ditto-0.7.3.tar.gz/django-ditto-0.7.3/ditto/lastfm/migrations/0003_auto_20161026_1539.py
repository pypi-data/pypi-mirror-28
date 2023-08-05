# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-26 15:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lastfm', '0002_auto_20161012_1012'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='original_slug',
            field=models.TextField(blank=True, help_text='As used on Last.fm. Mixed case.', null=True),
        ),
        migrations.AddField(
            model_name='artist',
            name='original_slug',
            field=models.TextField(blank=True, help_text='As used on Last.fm. Mixed case.', null=True),
        ),
        migrations.AddField(
            model_name='track',
            name='original_slug',
            field=models.TextField(blank=True, help_text='As used on Last.fm. Mixed case.', null=True),
        ),
        migrations.AlterField(
            model_name='album',
            name='slug',
            field=models.TextField(db_index=True, help_text='Lowercase'),
        ),
        migrations.AlterField(
            model_name='artist',
            name='slug',
            field=models.TextField(help_text='Lowercase', unique=True),
        ),
        migrations.AlterField(
            model_name='track',
            name='slug',
            field=models.TextField(db_index=True, help_text='Lowercase'),
        ),
    ]
