# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-02 10:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vsite', '0025_auto_20161123_1246'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemrecipes',
            name='recipe',
        ),
        migrations.AddField(
            model_name='itemrecipes',
            name='inga',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='self_ing_a', to='vsite.ItemRecipes'),
        ),
        migrations.AddField(
            model_name='itemrecipes',
            name='ingb',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='self_ing_b', to='vsite.ItemRecipes'),
        ),
        migrations.AddField(
            model_name='itemrecipes',
            name='ingc',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='self_ing_c', to='vsite.ItemRecipes'),
        ),
        migrations.AlterField(
            model_name='pjnote',
            name='pnj',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pnj_id', to='vsite.Pnj'),
        ),
    ]