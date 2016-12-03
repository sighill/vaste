# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-02 12:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vsite', '0028_auto_20161202_1309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemrecipes',
            name='description',
            field=models.CharField(blank=True, max_length=2048, null=True),
        ),
        migrations.AlterField(
            model_name='pjnote',
            name='pnj',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pnj_id', to='vsite.Pnj'),
        ),
    ]
