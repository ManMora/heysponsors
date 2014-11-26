# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.ForeignKey(related_name=b'Report', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Benefit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=140)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'Benefit',
                'verbose_name_plural': 'Benefits',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Concession',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=140)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'Concession',
                'verbose_name_plural': 'Concessions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=140)),
                ('description', models.TextField()),
                ('date', models.DateTimeField(default=datetime.datetime(2014, 11, 24, 21, 28, 39, 771651))),
                ('duration', models.TimeField()),
                ('link_map', models.CharField(max_length=140)),
                ('url_event', models.URLField(max_length=140)),
                ('budget', models.IntegerField()),
                ('goal', models.TextField()),
                ('active', models.BooleanField(default=1)),
                ('finished', models.BooleanField(default=0)),
                ('user', models.ForeignKey(related_name=b'Events', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LogActivity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(default=datetime.datetime(2014, 11, 24, 21, 28, 39, 775888))),
                ('content', models.TextField()),
                ('report', models.ForeignKey(related_name=b'Logs', to='sponsorsManager.ActivityReport')),
            ],
            options={
                'verbose_name_plural': 'Log activities',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Needs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=140)),
                ('description', models.TextField()),
                ('event', models.ForeignKey(related_name=b'Needs', to='sponsorsManager.Event')),
            ],
            options={
                'verbose_name': 'Needs',
                'verbose_name_plural': 'Needs',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sponsors',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=140)),
                ('logo', models.ImageField(upload_to=b'')),
                ('tel', phonenumber_field.modelfields.PhoneNumberField(max_length=128)),
                ('email', models.EmailField(max_length=75)),
                ('direccion', models.CharField(max_length=140)),
            ],
            options={
                'verbose_name': 'Sponsor',
                'verbose_name_plural': 'Sponsors',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sponsorship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=1)),
                ('finished', models.BooleanField(default=0)),
                ('benefits', models.ForeignKey(related_name=b'Sponsorships', to='sponsorsManager.Benefit')),
                ('concesions', models.ForeignKey(related_name=b'Sponsorships', to='sponsorsManager.Concession')),
                ('event', models.ForeignKey(related_name=b'Sponsorships', to='sponsorsManager.Event')),
                ('sponsor', models.ForeignKey(related_name=b'Sponsorships', to='sponsorsManager.Sponsors')),
            ],
            options={
                'verbose_name': 'Sponsorship',
                'verbose_name_plural': 'Sponsorships',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location_latitud', models.CharField(max_length=140)),
                ('location_altitud', models.CharField(max_length=140)),
                ('organization', models.CharField(max_length=140)),
                ('active', models.BooleanField(default=1)),
                ('user', models.ForeignKey(related_name=b'user_data', to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
                'verbose_name': 'User',
            },
            bases=(models.Model,),
        ),
    ]
