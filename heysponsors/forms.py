from django.db import models
from django.forms import ModelForm
from models import UserProfile

class AddUserProfileForm (ModelForm):

    class Meta:
        model = UserProfile
        fields = ['email', 'username', 'password']

class UpdateUserProfileForm (ModelForm):

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'email', 'username', 'password']


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['content']


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ['content']
