# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lamonte_core', '0003_auto_20160818_1030'),
    ]

    operations = [
        migrations.AddField(
            model_name='bag',
            name='macid',
            field=models.CharField(unique=True, null=True, blank=True, max_length=250),
        ),
    ]
