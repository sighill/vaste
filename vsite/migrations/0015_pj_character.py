# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-21 14:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vsite', '0014_home_items_order_position'),
    ]

    operations = [
        migrations.CreateModel(
            name='pj_character',
            fields=[
                ('uid', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('img_id', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('first_job', models.PositiveIntegerField(choices=[('Scaveux', 'Scaveux'), ('Fongerbeux', 'Fongerbeux'), ('Chassoux', 'Chassoux'), ('Soldards', 'Soldards'), ('Brassoux', 'Brassoux'), ('Chamans', 'Chamans')])),
                ('second_job', models.PositiveIntegerField(choices=[('Boisard', 'Boisard'), ('Forgeard', 'Forgeard'), ('Chefton', 'Chefton'), ('Soigneur', 'Soigneur'), ('Leveur', 'Leveur')])),
                ('attributes', models.CharField(default='0,0,0,0,0,0,0,0,0', max_length=100)),
                ('skills', models.CharField(blank=True, max_length=1200)),
                ('stuff', models.CharField(blank=True, max_length=1200)),
                ('more', models.CharField(blank=True, max_length=2500, null=True)),
                ('player_uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player_id', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]