# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-19 05:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapapp', '0009_auto_20170316_2345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='street',
            field=models.CharField(max_length=25, null=True),
        ),
    ]