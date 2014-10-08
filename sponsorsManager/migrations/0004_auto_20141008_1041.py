# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorsManager', '0003_auto_20141007_2358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 8, 10, 41, 6, 888520)),
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(unique=True, max_length=140),
        ),
    ]
