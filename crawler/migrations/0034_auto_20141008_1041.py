# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0033_auto_20141007_2358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='query',
            name='Timestamp',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 8, 10, 41, 6, 774631)),
        ),
    ]
