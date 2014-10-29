# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorsManager', '0002_auto_20141028_2243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 29, 3, 7, 10, 985000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='benefits',
            field=models.ForeignKey(related_name='Sponsorships', to='sponsorsManager.Benefit'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='concesions',
            field=models.ForeignKey(related_name='Sponsorships', to='sponsorsManager.Concession'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='event',
            field=models.ForeignKey(related_name='Sponsorships', to='sponsorsManager.Event'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='sponsor',
            field=models.ForeignKey(related_name='Sponsorships', to='sponsorsManager.Sponsors'),
            preserve_default=True,
        ),
    ]
