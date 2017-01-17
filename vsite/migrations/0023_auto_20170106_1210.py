# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-06 11:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vsite', '0022_auto_20170106_1207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='complete_file',
            field=models.CharField(blank=True, default='#', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='legend',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='legend_alt',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='ia_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='itemrecipes',
            name='ia',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='itemrecipes',
            name='ia_type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='itemrecipes',
            name='iaq',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='itemrecipes',
            name='ib',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='itemrecipes',
            name='ib_type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='itemrecipes',
            name='ibq',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='itemrecipes',
            name='ic',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='itemrecipes',
            name='ic_type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='itemrecipes',
            name='icq',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]