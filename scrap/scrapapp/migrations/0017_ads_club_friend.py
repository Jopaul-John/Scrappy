# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-26 13:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapapp', '0016_auto_20170322_0200'),
    ]

    operations = [
        migrations.AddField(
            model_name='ads',
            name='club_friend',
            field=models.BooleanField(default=False),
        ),
    ]
