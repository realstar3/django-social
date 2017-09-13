# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile, Company, Tag, Category

admin.site.register(Profile)
admin.site.register(Company)
admin.site.register(Tag)
admin.site.register(Category)