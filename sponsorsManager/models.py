from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    location_latitud = models.CharField(max_length=140)
    location_altitud = models.CharField(max_length=140)
    organization = models.CharField(max_length=140)

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class Event(models.Model):
    name = models.CharField(max_length=140)
    description = models.TextField()
    user = models.ForeignKey('UserProfile', related_name='Events')
    date = models.DateTimeField(blank=False, default=datetime.now())
    duration = models.TimeField(blank=False)
    link_map = models.CharField(max_length=140)
    url_event = models.URLField(max_length=140)
    team_members = models.ManyToManyField('UserProfile')
    budget = models.IntegerField()
    goal = models.TextField()

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"


class Needs(models.Model):
    event = models.ForeignKey('Event', related_name="Needs")
    name = models.CharField(max_length=140)
    description = models.TextField()

    class Meta:
        verbose_name = "Needs"
        verbose_name_plural = "Needs"


class Sponsors(models.Model):
    name = models.CharField(max_length=140)
    logo = models.ImageField()
    tel = PhoneNumberField()
    email = models.EmailField()
    direccion = models.CharField(max_length=140)
    categoria = models.ForeignKey('Sponsor_cat')

    class Meta:
        verbose_name = "Sponsor"
        verbose_name_plural = "Sponsors"


class Sponsor_cat(models.Model):
    name = models.CharField(max_length=140)
    description = models.TextField()

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Benefit(models.Model):
    name = models.CharField(max_length=140)
    description = models.TextField()

    class Meta:
        verbose_name = "Benefit"
        verbose_name_plural = "Benefits"


class Concession(models.Model):
    name = models.CharField(max_length=140)
    description = models.TextField()

    class Meta:
        verbose_name = "Concession"
        verbose_name_plural = "Concessions"


class Sponsorship(models.Model):
    sponsor = models.ForeignKey('Sponsors', related_name='Sponsorship')
    event = models.ForeignKey('Event', related_name='Sponsorship')
    benefits = models.ForeignKey('Benefit', related_name='Sponsorship')
    concesions = models.ForeignKey('Concession', related_name='Sponsorship')

    class Meta:
        verbose_name = "Sponsorship"
        verbose_name_plural = "Sponsorships"

