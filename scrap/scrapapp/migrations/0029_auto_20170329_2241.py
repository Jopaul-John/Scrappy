# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-29 17:11
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scrapapp', '0028_auto_20170329_2239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ads',
            name='expires',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 5, 22, 41, 12, 31495)),
        ),
        migrations.AlterField(
            model_name='expired_ad',
            name='ad',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='scrapapp.Ads'),
        ),
    ]
