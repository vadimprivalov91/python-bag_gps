# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lamonte_core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='devicedataentry',
            name='gps_valid',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='devicedataentry',
            name='gsm_signal_strength',
            field=models.CharField(max_length=64, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='devicedataentry',
            name='hdop',
            field=models.CharField(max_length=64, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='devicedataentry',
            name='num_of_satellite_used',
            field=models.CharField(max_length=64, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bag',
            name='imei',
            field=models.BigIntegerField(unique=True, verbose_name='IMEI'),
        ),
        migrations.AlterField(
            model_name='luser',
            name='email',
            field=models.EmailField(max_length=255, unique=True, verbose_name='email address'),
        ),
    ]
