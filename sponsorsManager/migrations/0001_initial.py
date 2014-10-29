# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import phonenumber_field.modelfields
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Benefit',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=140)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Benefits',
                'verbose_name': 'Benefit',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Concession',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=140)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Concessions',
                'verbose_name': 'Concession',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=140)),
                ('description', models.TextField()),
                ('date', models.DateTimeField(default=datetime.datetime(2014, 10, 28, 17, 6, 3, 793722))),
                ('duration', models.TimeField()),
                ('link_map', models.CharField(max_length=140)),
                ('url_event', models.URLField(max_length=140)),
                ('budget', models.IntegerField()),
                ('goal', models.TextField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='Events')),
            ],
            options={
                'verbose_name_plural': 'Events',
                'verbose_name': 'Event',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Needs',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=140)),
                ('description', models.TextField()),
                ('event', models.ForeignKey(to='sponsorsManager.Event', related_name='Needs')),
            ],
            options={
                'verbose_name_plural': 'Needs',
                'verbose_name': 'Needs',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sponsor_cat',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=140)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'verbose_name': 'Category',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sponsors',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=140)),
                ('logo', models.ImageField(upload_to='')),
                ('tel', phonenumber_field.modelfields.PhoneNumberField(max_length=128)),
                ('email', models.EmailField(max_length=75)),
                ('direccion', models.CharField(max_length=140)),
                ('categoria', models.ForeignKey(to='sponsorsManager.Sponsor_cat')),
            ],
            options={
                'verbose_name_plural': 'Sponsors',
                'verbose_name': 'Sponsor',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sponsorship',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('benefits', models.ForeignKey(to='sponsorsManager.Benefit', related_name='Sponsorship')),
                ('concesions', models.ForeignKey(to='sponsorsManager.Concession', related_name='Sponsorship')),
                ('event', models.ForeignKey(to='sponsorsManager.Event', related_name='Sponsorship')),
                ('sponsor', models.ForeignKey(to='sponsorsManager.Sponsors', related_name='Sponsorship')),
            ],
            options={
                'verbose_name_plural': 'Sponsorships',
                'verbose_name': 'Sponsorship',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('location_latitud', models.CharField(max_length=140)),
                ('location_altitud', models.CharField(max_length=140)),
                ('organization', models.CharField(max_length=140)),
                ('active', models.BooleanField(default=1)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='user_data', unique=True)),
            ],
            options={
                'verbose_name': 'User',
            },
            bases=(models.Model,),
        ),
    ]
