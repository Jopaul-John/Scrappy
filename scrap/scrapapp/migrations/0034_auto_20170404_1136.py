# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-04 06:06
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapapp', '0033_auto_20170404_1043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ads',
            name='expires',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 11, 11, 36, 2, 387385)),
        ),
    ]