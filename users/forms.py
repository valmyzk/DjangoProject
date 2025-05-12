import django.contrib.auth.forms
from django.contrib import auth
from django import forms

from .models import User

class UserCreationForm(auth.forms.UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'phone', 'date_of_birth')
        widgets = {
            'date_of_birth': forms.DateInput({'type': 'date'}),
            'phone': forms.TextInput({'type': 'tel'})
        }

class UserChangeForm(auth.forms.UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'phone', 'date_of_birth')