# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-01-15 04:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('online', '0011_tournamentplayers_enabled_in_pantheon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tournamentgameplayer',
            name='is_active',
        ),
    ]
