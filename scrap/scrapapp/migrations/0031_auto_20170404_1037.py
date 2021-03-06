# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-04 05:07
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scrapapp', '0030_auto_20170404_1000'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductProfit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sell_price', models.IntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scrapapp.Product')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='scrapapp.UserProfile')),
            ],
        ),
        migrations.RemoveField(
            model_name='profit',
            name='sell_price',
        ),
        migrations.AlterField(
            model_name='ads',
            name='expires',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 11, 10, 37, 48, 795319)),
        ),
        migrations.AlterField(
            model_name='profit',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scrapapp.ProductProfit'),
        ),
    ]
