# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0026_auto_20140910_0240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='query',
            name='Timestamp',
            field=models.DateTimeField(default=datetime.datetime(2014, 9, 10, 2, 45, 30, 785820)),
        ),
    ]
