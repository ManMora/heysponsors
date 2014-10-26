# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorsManager', '0005_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 25, 23, 58, 35, 780475)),
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(max_length=140),
        ),
        migrations.AlterField(
            model_name='needs',
            name='event',
            field=models.ForeignKey(to='sponsorsManager.Event', related_name='Needs'),
        ),
    ]
