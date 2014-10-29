# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorsManager', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sponsors',
            name='categoria',
        ),
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 28, 22, 43, 50, 896000)),
            preserve_default=True,
        ),
    ]
