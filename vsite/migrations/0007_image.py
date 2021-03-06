# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-05 09:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vsite', '0006_remove_changelog_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('uid', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('internal_link', models.CharField(max_length=500)),
                ('external_link', models.CharField(max_length=500)),
                ('legend', models.CharField(max_length=500)),
                ('legend_alt', models.CharField(max_length=500)),
                ('complete_file', models.CharField(max_length=500)),
            ],
        ),
    ]
