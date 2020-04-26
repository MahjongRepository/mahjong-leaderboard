# Generated by Django 2.2.10 on 2020-02-22 11:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0009_playerwrc'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerQuotaEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('place', models.PositiveIntegerField(blank=True, default=None, null=True)),
                ('score', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=10, null=True)),
                ('state', models.PositiveSmallIntegerField(choices=[[0, 'точно едет'], [1, 'скорее всего едет'], [2, 'пока сомневается, но скорее всего не едет'], [3, 'игрок пока ничего не ответил'], [4, 'игрок пока что не проходит, но готов ехать, если появится квота'], [5, 'точно не едет'], [6, 'чемпион'], [7, 'игрок замены'], [8, 'судья'], [9, 'новая запись']], default=9)),
                ('federation_member', models.BooleanField(default=False, null=True)),
                ('type', models.PositiveSmallIntegerField(choices=[[0, 'ERMC 2019'], [1, 'WRC 2020']])),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='player.Player')),
            ],
            options={
                'ordering': ['place'],
            },
        ),
    ]