# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-26 14:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapapp', '0017_ads_club_friend'),
    ]

    operations = [
        migrations.AddField(
            model_name='ads',
            name='is_bidded',
            field=models.BooleanField(default=False),
        ),
    ]