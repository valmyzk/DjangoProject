import django.contrib.auth.forms
from django import forms
from django.contrib import auth

from .models import User

BOOTSTRAP_ATTRS = {'class': 'form-control bg-dark text-white border-secondary'}


class UserCreationForm(auth.forms.UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'phone', 'date_of_birth')
        widgets = {
            'email': forms.EmailInput(BOOTSTRAP_ATTRS),
            'phone': forms.TextInput(BOOTSTRAP_ATTRS | {'type': 'tel'}),
            'date_of_birth': forms.DateInput(BOOTSTRAP_ATTRS | {'type': 'date'})
        }


class UserChangeForm(auth.forms.UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'phone', 'date_of_birth')
