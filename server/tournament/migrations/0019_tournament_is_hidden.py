# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-06-16 13:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0018_remove_tournament_has_accreditation'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='is_hidden',
            field=models.BooleanField(default=False),
        ),
    ]
