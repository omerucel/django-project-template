#-*- coding: utf-8 -*-

import datetime

from django.contrib import admin
from django.contrib import messages
from models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'facebook_id')
    ordering = ('user',)
    raw_id_fields = ('user',)

admin.site.register(Profile, ProfileAdmin)