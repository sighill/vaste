# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-05 11:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vsite', '0013_auto_20170105_1234'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gameentity',
            old_name='image',
            new_name='img_name',
        ),
        migrations.RenameField(
            model_name='gamelog',
            old_name='image',
            new_name='img_name',
        ),
        migrations.RenameField(
            model_name='homeitems',
            old_name='image',
            new_name='img_name',
        ),
    ]
