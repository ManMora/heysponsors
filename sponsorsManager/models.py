from datetime import datetime
from django.db import models
from django.contrib.auth.models import User, UserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True, related_name='user_data')
    #user = models.OneToOneField(User, related_name='profile')
    location_latitud = models.CharField(max_length=140)
    location_altitud = models.CharField(max_length=140)
    organization = models.CharField(max_length=140)
    active = models.BooleanField(default=1)
    class Meta:
        verbose_name = "User"
    
    def __str__(self):
        return self.user.username

    def select_events(self):
        return self.select_related('Events')

    def is_active(self):
        return self.active

class Event(models.Model):
    name = models.CharField(max_length=140, unique=False)
    description = models.TextField()
    user = models.ForeignKey(User, related_name='Events')
    date = models.DateTimeField(blank=False, default=datetime.now())
    duration = models.TimeField(blank=False)
    link_map = models.CharField(max_length=140)
    url_event = models.URLField(max_length=140)
    ##team_members = models.ManyToManyField(User)
    budget = models.IntegerField()
    goal = models.TextField()

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def __str__(self):
        return self.name


class Needs(models.Model):
    event = models.ForeignKey('Event', related_name="Needs", unique=False)
    name = models.CharField(max_length=140)
    description = models.TextField()

    class Meta:
        verbose_name = "Needs"
        verbose_name_plural = "Needs"

    def __str__(self):
        return self.name


class Sponsors(models.Model):
    name = models.CharField(max_length=140)
    logo = models.ImageField()
    tel = PhoneNumberField()
    email = models.EmailField()
    direccion = models.CharField(max_length=140)

    class Meta:
        verbose_name = "Sponsor"
        verbose_name_plural = "Sponsors"

    def __str__(self):
        return self.name + " , " + self.direccion


class Sponsor_cat(models.Model):
    name = models.CharField(max_length=140)
    description = models.TextField()

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Benefit(models.Model):
    name = models.CharField(max_length=140)
    description = models.TextField()

    class Meta:
        verbose_name = "Benefit"
        verbose_name_plural = "Benefits"

    def __str__(self):
        return self.name


class Concession(models.Model):
    name = models.CharField(max_length=140)
    description = models.TextField()

    class Meta:
        verbose_name = "Concession"
        verbose_name_plural = "Concessions"

    def __str__(self):
        return self.name


class Sponsorship(models.Model):
    sponsor = models.ForeignKey('Sponsors', related_name='Sponsorships')
    event = models.ForeignKey('Event', related_name='Sponsorships')
    benefits = models.ForeignKey('Benefit', related_name='Sponsorships')
    concesions = models.ForeignKey('Concession', related_name='Sponsorships')

    class Meta:
        verbose_name = "Sponsorship"
        verbose_name_plural = "Sponsorships"

    def __str__(self):
        return str(self.sponsor) + str(self.event)
