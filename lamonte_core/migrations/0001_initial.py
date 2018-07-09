# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from lamonte import settings
import lamonte_core.models
import django.utils.timezone
import django.core.validators
import django.contrib.auth.models
import lamonte_core.models
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='LUser',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('is_admin', models.BooleanField(default=False)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(unique=True, max_length=255, verbose_name=b'email address')),
                ('is_active', models.BooleanField(default=True)),
                ('is_user_add_api_account', models.BooleanField(default=False)),
                ('lat', models.FloatField(null=True, blank=True)),
                ('lon', models.FloatField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
            },
            managers=[],
        ),
        migrations.CreateModel(
            name='Bag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=1024, db_index=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('imei', models.BigIntegerField(unique=True, verbose_name=b'IMEI')),
                ('geo_fence', models.FloatField(default=10)),
                ('tracking', models.BooleanField(default=True, db_index=True)),
                ('lat', models.FloatField(null=True, blank=True)),
                ('lon', models.FloatField(null=True, blank=True)),
                ('altitude', models.FloatField(null=True, blank=True)),
                ('speed', models.FloatField(null=True, blank=True)),
                ('distance', models.FloatField(null=True, blank=True)),
                ('battery', models.FloatField(default=1, validators=[django.core.validators.MinValueValidator(0),
                                                                     django.core.validators.MaxValueValidator(1)])),
                ('charging', models.BooleanField(default=False)),
                ('image', imagekit.models.fields.ProcessedImageField(null=True, upload_to=lamonte_core.models.image_path, blank=True)),
                ('nearby', models.BooleanField(default=False, db_index=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Bag',
                'verbose_name_plural': 'Bags',
            },
        ),
        migrations.AlterModelOptions(
            name='LUser',
            options={'verbose_name_plural': 'Users', 'verbose_name': 'User'},
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=1024, db_index=True)),
                ('iso', models.CharField(max_length=3)),
                ('phone', models.CharField(max_length=1024)),
                ('e164Phone', models.CharField(max_length=1024)),
                ('formattedPhone', models.CharField(max_length=1024)),
                ('bag', models.ForeignKey(related_name='contacts', to='lamonte_core.Bag')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Contact Assigned for Bag',
                'verbose_name_plural': 'Contacts Assigned for Bag',
            },
        ),
        migrations.CreateModel(
            name='DeviceDataEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('data', models.TextField()),
                ('altitude', models.FloatField(null=True, blank=True)),
                ('battery', models.FloatField(null=True, blank=True)),
                ('cell_id', models.IntegerField(null=True, blank=True)),
                ('coarse', models.FloatField(null=True, blank=True)),
                ('imei', models.BigIntegerField(db_index=True, null=True, blank=True)),
                ('lat', models.FloatField(null=True, blank=True)),
                ('lon', models.FloatField(null=True, blank=True)),
                ('speed', models.FloatField(null=True, blank=True)),
                ('temperature', models.FloatField(null=True, blank=True)),
                ('timestamp', models.IntegerField(null=True, blank=True)),
                ('wifi_mac_id_1', models.CharField(max_length=64, blank=True)),
                ('wifi_mac_id_2', models.CharField(max_length=64, blank=True)),
                ('wifi_mac_id_3', models.CharField(max_length=64, blank=True)),
                ('wifi_mac_id_4', models.CharField(max_length=64, blank=True)),
                ('wifi_mac_id_5', models.CharField(max_length=64, blank=True)),
                ('wifi_ssid_1', models.CharField(max_length=32, blank=True)),
                ('wifi_ssid_2', models.CharField(max_length=32, blank=True)),
                ('wifi_ssid_3', models.CharField(max_length=32, blank=True)),
                ('wifi_ssid_4', models.CharField(max_length=32, blank=True)),
                ('wifi_ssid_5', models.CharField(max_length=32, blank=True)),
                ('bag', models.ForeignKey(related_name='device_data_entries', blank=True, to='lamonte_core.Bag', null=True)),
            ],
            options={
                'ordering': ['-created'],
                'verbose_name': 'Device Data Entry',
                'verbose_name_plural': 'Device Data Entries',
            },
        ),
    ]
