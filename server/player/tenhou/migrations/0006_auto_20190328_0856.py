# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-03-28 08:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tenhou', '0005_tenhounickname_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='TenhouAggregatedStatistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.PositiveSmallIntegerField(choices=[[0, '新人'], [1, '９級'], [2, '８級'], [3, '７級'], [4, '６級'], [5, '５級'], [6, '４級'], [7, '３級'], [8, '２級'], [9, '１級'], [10, '初段'], [11, '二段'], [12, '三段'], [13, '四段'], [14, '五段'], [15, '六段'], [16, '七段'], [17, '八段'], [18, '九段'], [19, '十段'], [20, '天鳳位']])),
                ('rate', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('game_type', models.PositiveSmallIntegerField(blank=True, choices=[[0, 'Four players'], [1, 'Three players']], null=True)),
                ('played_games', models.PositiveIntegerField(default=0)),
                ('month_played_games', models.PositiveIntegerField(default=0)),
                ('average_place', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('month_average_place', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('pt', models.PositiveSmallIntegerField(default=0)),
                ('end_pt', models.PositiveSmallIntegerField(default=0)),
                ('tenhou_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aggregated_statistics', to='tenhou.TenhouNickname')),
            ],
            options={
                'db_table': 'portal_tenhou_aggregated_statistics',
            },
        ),
        migrations.AddField(
            model_name='tenhougamelog',
            name='game_players',
            field=models.PositiveSmallIntegerField(blank=True, choices=[[0, 'Four players'], [1, 'Three players']], null=True),
        ),
    ]
