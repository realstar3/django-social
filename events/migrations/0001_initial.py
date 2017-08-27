# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-27 10:35
from __future__ import unicode_literals

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('image', models.ImageField(blank=True, null=True, upload_to='event_images/%Y/%m/%d/')),
                ('start_date', models.DateTimeField(null=True, verbose_name='start date')),
                ('description', tinymce.models.HTMLField(blank=True, null=True)),
                ('detail', tinymce.models.HTMLField(blank=True, null=True)),
                ('pub_date', models.DateTimeField(null=True, verbose_name='date published')),
                ('featured', models.BooleanField(default=False)),
                ('event_url', models.CharField(max_length=150, null=True)),
            ],
        ),
    ]
