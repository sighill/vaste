# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-06 14:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vsite', '0023_auto_20170106_1210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='external_link',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
