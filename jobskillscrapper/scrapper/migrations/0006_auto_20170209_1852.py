# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-09 18:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapper', '0005_auto_20170208_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parsedprofile',
            name='url',
            field=models.URLField(max_length=250, unique=True),
        ),
    ]
