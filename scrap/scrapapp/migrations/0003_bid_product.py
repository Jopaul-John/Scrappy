# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-04 16:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapapp', '0002_auto_20170304_2149'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='product',
            field=models.CharField(default='', max_length=20),
        ),
    ]
