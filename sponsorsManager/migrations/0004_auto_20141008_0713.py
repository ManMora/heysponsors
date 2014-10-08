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
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 8, 7, 13, 0, 645975)),
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(max_length=140, unique=True),
        ),
        migrations.AlterField(
            model_name='needs',
            name='event',
            field=models.ForeignKey(related_name='Needs', unique=True, to='sponsorsManager.Event'),
        ),
    ]
