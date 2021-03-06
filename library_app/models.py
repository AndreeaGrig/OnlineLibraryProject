# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.files.storage import FileSystemStorage
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from OnlineLibrary import settings


class Book(models.Model):
    title = models.CharField(max_length=100)
    category = models.IntegerField(choices=[
        (1, "Art"),
        (2, "Fantasy"),
        (3, "Biographies"),
        (4, "Science"),
        (5, "Romance"),
        (6, "Religion"),
        (7, "Children"),
        (8, "History"),
    ]
    )
    author = models.CharField(max_length=300)
    description = models.TextField(max_length=10000)
    type = models.IntegerField(choices=[
        (1, "Premium"),
        (2, "Standard"),
    ]
    )
    add_date = models.DateTimeField(auto_now_add=True)
    pub_date = models.DateTimeField()
    pub_house = models.CharField(max_length=300)
    pdf = models.FileField(storage=FileSystemStorage(location=settings.MEDIA_ROOT), upload_to='pdfs')
    cover = models.ImageField(upload_to='covers')
    price = models.FloatField()


class Purchase(models.Model):
    id_book = models.ForeignKey(Book, on_delete=models.CASCADE)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    text = models.TextField(max_length=10000)
    id_book = models.ForeignKey(Book)
    id_user = models.ForeignKey(User)
    posted = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    id_book = models.ForeignKey(Book)
    tag_name = models.CharField(max_length=300)
