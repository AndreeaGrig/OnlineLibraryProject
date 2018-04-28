# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-28 18:26
from __future__ import unicode_literals

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0006_merge_20180428_1938'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.AlterField(
            model_name='book',
            name='pdf',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(location=b'C:\\Users\\User\\Documents\\GitHub\\OnlineLibraryProject\\media'), upload_to='pdfs'),
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
