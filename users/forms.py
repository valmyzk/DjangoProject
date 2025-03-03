from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser

class SignupForm(UserCreationForm):
    full_name = forms.CharField(max_length=255, help_text='Required')
    email = forms.EmailField(max_length=200, help_text='Required')


    class Meta:
        model = CustomUser
        fields = ('full_name','email','username', 'email', 'password1', 'password2')