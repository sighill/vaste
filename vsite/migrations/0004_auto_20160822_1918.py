# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-22 17:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vsite', '0003_auto_20160822_1204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pnj',
            name='description',
            field=models.TextField(blank=True, max_length=2000, null=True),
        ),
    ]