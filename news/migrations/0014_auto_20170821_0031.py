# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-21 00:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0013_news_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='article_text',
        ),
        migrations.RemoveField(
            model_name='news',
            name='featured_image',
        ),
        migrations.RemoveField(
            model_name='news',
            name='image',
        ),
    ]
