# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lamonte_core', '0004_bag_macid'),
    ]

    operations = [
        migrations.AddField(
            model_name='luser',
            name='name',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
    ]
