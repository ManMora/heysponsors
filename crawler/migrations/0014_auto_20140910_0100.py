# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0013_auto_20140909_2102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='query',
            name='Timestamp',
            field=models.DateTimeField(default=datetime.datetime(2014, 9, 10, 1, 0, 40, 784999)),
        ),
    ]