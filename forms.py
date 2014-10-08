from django.db import models
from django.forms import ModelForm
from django import forms
from sponsorsManager.models import UserProfile
from sponsorsManager.models import Event
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username","email", "password"]

class UserCreateForm(forms.ModelForm):
    """email = forms.EmailField(
        max_length=75, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    organization = forms.CharField(
        max_length=140, widget=forms.TextInput(
            attrs={'placeholder': 'Organization'}))"""
    class Meta:
        model = UserProfile
        fields = []

class UserEditForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password"]

class UserProfileEditForm(forms.ModelForm):
    """email = forms.EmailField(
        max_length=75, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    organization = forms.CharField(
        max_length=140, widget=forms.TextInput(
            attrs={'placeholder': 'Organization'}))"""
    class Meta:
        model = UserProfile
        fields = ['organization']


class EventCreateForm(ModelForm):
	class Meta:
		model = Event
		fields = ['name', 'description', 'date', 'duration',
			'link_map', 'url_event', 'budget', 'goal']
