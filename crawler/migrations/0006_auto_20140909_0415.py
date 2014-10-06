# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0005_auto_20140909_0414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='query',
            name='Timestamp',
            field=models.DateTimeField(default=datetime.datetime(2014, 9, 9, 4, 15, 23, 406176)),
        ),
    ]
