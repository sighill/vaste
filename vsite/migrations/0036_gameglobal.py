# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-02 07:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vsite', '0035_auto_20170126_1708'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameGlobal',
            fields=[
                ('uid', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('value', models.CharField(max_length=255)),
            ],
        ),
    ]
