# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-04 05:10
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scrapapp', '0031_auto_20170404_1037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ads',
            name='expires',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 11, 10, 40, 40, 329210)),
        ),
        migrations.AlterField(
            model_name='profit',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='scrapapp.ProductProfit'),
        ),
        migrations.AlterField(
            model_name='profit',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scrapapp.UserProfile'),
        ),
    ]
