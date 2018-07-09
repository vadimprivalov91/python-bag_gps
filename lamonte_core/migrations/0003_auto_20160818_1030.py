# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lamonte_core', '0002_auto_20160812_1041'),
    ]

    operations = [
        migrations.CreateModel(
            name='LatestDeviceDataEntry',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('data', models.TextField()),
                ('imei', models.BigIntegerField(blank=True, db_index=True, null=True)),
                ('timestamp', models.IntegerField(blank=True, null=True)),
                ('lat', models.FloatField(blank=True, null=True)),
                ('lon', models.FloatField(blank=True, null=True)),
                ('speed', models.FloatField(blank=True, null=True)),
                ('coarse', models.FloatField(blank=True, null=True)),
                ('cell_id', models.IntegerField(blank=True, null=True)),
                ('battery', models.FloatField(blank=True, null=True)),
                ('altitude', models.FloatField(blank=True, null=True)),
                ('temperature', models.FloatField(blank=True, null=True)),
                ('wifi_ssid_1', models.CharField(blank=True, max_length=32)),
                ('wifi_ssid_2', models.CharField(blank=True, max_length=32)),
                ('wifi_ssid_3', models.CharField(blank=True, max_length=32)),
                ('wifi_ssid_4', models.CharField(blank=True, max_length=32)),
                ('wifi_ssid_5', models.CharField(blank=True, max_length=32)),
                ('wifi_mac_id_1', models.CharField(blank=True, max_length=64)),
                ('wifi_mac_id_2', models.CharField(blank=True, max_length=64)),
                ('wifi_mac_id_3', models.CharField(blank=True, max_length=64)),
                ('wifi_mac_id_4', models.CharField(blank=True, max_length=64)),
                ('wifi_mac_id_5', models.CharField(blank=True, max_length=64)),
                ('gsm_signal_strength', models.CharField(blank=True, max_length=64, null=True)),
                ('hdop', models.CharField(blank=True, max_length=64, null=True)),
                ('num_of_satellite_used', models.CharField(blank=True, verbose_name='Number of satellite used for fix', max_length=64, null=True)),
                ('gps_valid', models.IntegerField(blank=True, null=True)),
                ('bag', models.ForeignKey(blank=True, related_name='device_data_entry', to='lamonte_core.Bag', null=True)),
            ],
            options={
                'verbose_name_plural': 'Latest Device Data Entries',
                'verbose_name': 'Latest Device Data Entry',
                'ordering': ['-created'],
            },
        ),
        migrations.AlterField(
            model_name='devicedataentry',
            name='num_of_satellite_used',
            field=models.CharField(blank=True, verbose_name='Number of satellite used for fix', max_length=64, null=True),
        ),
    ]
