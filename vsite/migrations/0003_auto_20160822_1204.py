# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-22 10:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vsite', '0002_remove_pnj_url_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pnj',
            name='img_id',
            field=models.CharField(blank=True, max_length=2500, null=True),
        ),
    ]