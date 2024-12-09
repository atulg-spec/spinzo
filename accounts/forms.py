# accounts/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    phone_number = forms.CharField(max_length=15)
