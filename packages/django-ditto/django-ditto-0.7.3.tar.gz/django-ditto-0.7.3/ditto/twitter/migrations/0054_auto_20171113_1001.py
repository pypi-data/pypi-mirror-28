# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-13 10:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0053_tweet_post_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(help_text="eg, 'Samuel Pepys'", max_length=50),
        ),
    ]
