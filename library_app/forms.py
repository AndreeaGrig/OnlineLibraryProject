from unittest import loader

from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.utils.http import urlsafe_base64_encode
from jwt.utils import force_bytes

from .models import Review, Purchase
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ('text',)


class BookForm(forms.ModelForm):

    class Meta:
        model = Purchase
        fields = ()
