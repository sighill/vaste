# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-19 12:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vsite', '0031_auto_20170119_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='close_to',
            field=models.ManyToManyField(blank=True, related_name='_place_close_to_+', to='vsite.Place'),
        ),
    ]
