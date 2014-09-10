from django.db import models
from django.forms import ModelForm
from django import forms
from sponsorsManager.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(max_length=75,widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    organization = forms.CharField(max_length=140,widget=forms.TextInput(attrs={'placeholder': 'Organization'}))
    class Meta:
        model = User
        fields = ('username', 'email', 'organization', 'password1')
	
	

