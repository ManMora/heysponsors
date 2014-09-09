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
            name='Benefit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=140)),
                ('description', models.TextField()),
                ('date', models.DateTimeField(default=datetime.datetime(2014, 9, 7, 22, 2, 6, 788624))),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=140)),
                ('description', models.TextField()),
                ('event', models.ForeignKey(related_name='Needs', to='sponsorsManager.Event')),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('benefits', models.ForeignKey(related_name='Sponsorship', to='sponsorsManager.Benefit')),
                ('concesions', models.ForeignKey(related_name='Sponsorship', to='sponsorsManager.Concession')),
                ('event', models.ForeignKey(related_name='Sponsorship', to='sponsorsManager.Event')),
                ('sponsor', models.ForeignKey(related_name='Sponsorship', to='sponsorsManager.Sponsors')),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('location_latitud', models.CharField(max_length=140)),
                ('location_altitud', models.CharField(max_length=140)),
                ('organization', models.CharField(max_length=140)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
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
            field=models.ForeignKey(related_name='Events', to='sponsorsManager.UserProfile'),
            preserve_default=True,
        ),
    ]
