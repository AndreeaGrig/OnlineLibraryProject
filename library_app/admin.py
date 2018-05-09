# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from library_app.models import Book, Review, Purchase, Tag

# Register your models here.
admin.site.register(Book)
admin.site.register(Review)
admin.site.register(Purchase)
admin.site.register(Tag)


