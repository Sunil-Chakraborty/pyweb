# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Account

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=255, help_text='Required. Add a valid email address.')
    password = forms.CharField(widget=forms.PasswordInput)
