# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-20 20:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapapp', '0013_userprofile_ratings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='ratings',
            field=models.IntegerField(),
        ),
    ]
