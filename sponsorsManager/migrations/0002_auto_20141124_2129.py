# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorsManager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 24, 21, 29, 5, 126510)),
        ),
        migrations.AlterField(
            model_name='logactivity',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 24, 21, 29, 5, 130796)),
        ),
    ]
