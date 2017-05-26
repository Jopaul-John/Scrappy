# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-04 05:13
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scrapapp', '0032_auto_20170404_1040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ads',
            name='expires',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 11, 10, 43, 0, 151241)),
        ),
        migrations.AlterField(
            model_name='productprofit',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scrapapp.UserProfile'),
        ),
    ]