# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-06 11:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vsite', '0021_changelog_is_announce'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='complete_file',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='legend',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='legend_alt',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='ia_type',
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='itemrecipes',
            name='ia',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='itemrecipes',
            name='ia_type',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='itemrecipes',
            name='iaq',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='itemrecipes',
            name='ib',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='itemrecipes',
            name='ib_type',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='itemrecipes',
            name='ibq',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='itemrecipes',
            name='ic',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='itemrecipes',
            name='ic_type',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='itemrecipes',
            name='icq',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
    ]