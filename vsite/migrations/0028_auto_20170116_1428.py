# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-16 13:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vsite', '0027_auto_20170116_1417'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='img_name',
        ),
        migrations.AddField(
            model_name='item',
            name='img_name',
            field=models.ForeignKey(blank=True, default=39, on_delete=django.db.models.deletion.CASCADE, related_name='img_name_igi', to='vsite.Image'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='itemrecipes',
            name='img_name',
        ),
        migrations.AddField(
            model_name='itemrecipes',
            name='img_name',
            field=models.ForeignKey(blank=True, default=39, on_delete=django.db.models.deletion.CASCADE, related_name='img_name_ir', to='vsite.Image'),
            preserve_default=False,
        ),
    ]
