# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-31 07:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vsite', '0003_remove_pnj_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='is_visible',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='entity_uid', to='vsite.GameEntity'),
        ),
    ]