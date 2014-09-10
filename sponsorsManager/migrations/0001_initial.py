# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import phonenumber_field.modelfields
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Benefit',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
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
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
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
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=140)),
                ('description', models.TextField()),
                ('date', models.DateTimeField(default=datetime.datetime(2014, 9, 10, 2, 52, 52, 939726))),
                ('duration', models.TimeField()),
                ('link_map', models.CharField(max_length=140)),
                ('url_event', models.URLField(max_length=140)),
                ('budget', models.IntegerField()),
                ('goal', models.TextField()),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Needs',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=140)),
                ('description', models.TextField()),
                ('event', models.ForeignKey(to='sponsorsManager.Event', related_name='Needs')),
            ],
            options={
                'verbose_name': 'Needs',
                'verbose_name_plural': 'Needs',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sponsor_cat',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=140)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sponsors',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=140)),
                ('logo', models.ImageField(upload_to='')),
                ('tel', phonenumber_field.modelfields.PhoneNumberField(max_length=128)),
                ('email', models.EmailField(max_length=75)),
                ('direccion', models.CharField(max_length=140)),
                ('categoria', models.ForeignKey(to='sponsorsManager.Sponsor_cat')),
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
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('benefits', models.ForeignKey(to='sponsorsManager.Benefit', related_name='Sponsorship')),
                ('concesions', models.ForeignKey(to='sponsorsManager.Concession', related_name='Sponsorship')),
                ('event', models.ForeignKey(to='sponsorsManager.Event', related_name='Sponsorship')),
                ('sponsor', models.ForeignKey(to='sponsorsManager.Sponsors', related_name='Sponsorship')),
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
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('location_latitud', models.CharField(max_length=140)),
                ('location_altitud', models.CharField(max_length=140)),
                ('organization', models.CharField(max_length=140)),
                ('user', models.ForeignKey(unique=True, to=settings.AUTH_USER_MODEL, related_name='user_data')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='event',
            name='team_members',
            field=models.ManyToManyField(to='sponsorsManager.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='user',
            field=models.ForeignKey(to='sponsorsManager.UserProfile', related_name='Events'),
            preserve_default=True,
        ),
    ]
