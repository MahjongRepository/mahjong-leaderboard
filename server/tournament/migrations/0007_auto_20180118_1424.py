# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-18 14:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0003_delete_tournamenttype'),
        ('player', '0001_initial'),
        ('tournament', '0006_auto_20180118_1357'),
    ]

    operations = [
        migrations.CreateModel(
            name='OnlineTournamentRegistration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('is_approved', models.BooleanField(default=True)),
                ('first_name', models.CharField(max_length=255, verbose_name='First name')),
                ('last_name', models.CharField(max_length=255, verbose_name='Last name')),
                ('city', models.CharField(max_length=255, verbose_name='City')),
                ('tenhou_nickname', models.CharField(max_length=255, verbose_name='Tenhou.net nickname')),
                ('contact', models.CharField(help_text='It will be visible only to the tournament administrator', max_length=255, verbose_name='Your contact (email, phone, etc.)')),
                ('city_object', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='settings.City')),
                ('player', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='online_tournament_registrations', to='player.Player')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='tournament',
            name='tournament_type',
            field=models.CharField(choices=[['rr', 'rr'], ['crr', 'crr'], ['ema', 'ema'], ['fema', 'fema'], ['other', 'other'], ['online', 'online']], default='rr', max_length=10),
        ),
        migrations.AddField(
            model_name='onlinetournamentregistration',
            name='tournament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='online_tournament_registrations', to='tournament.Tournament'),
        ),
    ]
