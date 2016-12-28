# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-18 14:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vsite', '0036_auto_20161208_0921'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pjcharacter',
            name='large_img_id',
        ),
        migrations.RemoveField(
            model_name='pnj',
            name='large_img_id',
        ),
        migrations.AlterField(
            model_name='pjnote',
            name='pnj',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pnj_id', to='vsite.Pnj'),
        ),
    ]