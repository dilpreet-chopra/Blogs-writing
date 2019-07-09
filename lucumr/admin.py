# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Blog,Tag

admin.site.site_header = "lucumr-admin"
class InlineTag(admin.StackedInline):
    model = Tag
    extra = 1
    fields = ['tag']

class CelebrityAdmin(admin.ModelAdmin):
    
   inlines = [InlineTag]

admin.site.register(Blog,CelebrityAdmin)

class PersonAdmin(admin.ModelAdmin):
    pass