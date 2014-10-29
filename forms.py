from django.db import models
from django.forms import ModelForm, Form
from django import forms
from sponsorsManager.models import UserProfile, Concession
from sponsorsManager.models import Sponsors, Sponsorship
from sponsorsManager.models import Event, Needs, Benefit
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username","email", "password"]

class UserCreateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = []

class UserEditForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(required = False)
    last_name = forms.CharField(required = False)
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password"]

class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['organization']


class EventCreateForm(ModelForm):
    description = forms.CharField(required=False, widget=forms.Textarea)
    link_map = forms.CharField(required=False)
    url_event = forms.URLField(required=False)
    goal = forms.CharField(required=False, widget=forms.Textarea)

    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'duration',
			'link_map', 'url_event', 'budget', 'goal']


class EventReadForm(ModelForm):
    description = forms.CharField(required=False, widget=forms.Textarea)
    link_map = forms.CharField(required=False)
    url_event = forms.URLField(required=False)
    goal = forms.CharField(required=False, widget=forms.Textarea)


    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'duration',
            'link_map', 'url_event', 'budget', 'goal']

class NeedsCreateForm(ModelForm):
    event = models.ForeignKey('Event', related_name="Needs")
    name = models.CharField(max_length=140)

    class Meta:
        model = Needs
        fields = ['name', 'description']

class SponsorshipCreateForm(ModelForm):
    benefits_2 = forms.CharField(widget=forms.Textarea, required=False)
    concesions_2 = forms.CharField(widget=forms.Textarea, required=False)
    class Meta:
        model = Sponsors
        fields = ['benefits_2', 'concesions_2']

class BenefitsCreateForm(ModelForm):
    class Meta:
        model = Benefit
        fields = ['name', 'description']

class ConcessionsCreateForm(ModelForm):
    class Meta:
        model = Concession
        fields = ['name', 'description']

