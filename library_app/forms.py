from django import forms
from .models import Review


class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ('text',)

