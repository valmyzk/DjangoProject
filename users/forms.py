import django.contrib.auth.forms
from django import forms
from django.contrib import auth
from django.contrib.auth.forms import PasswordChangeForm

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
        widgets = {
            'email': forms.EmailInput(BOOTSTRAP_ATTRS),
            'phone': forms.TextInput(BOOTSTRAP_ATTRS | {'type': 'tel'}),
            'date_of_birth': forms.DateInput(BOOTSTRAP_ATTRS | {'type': 'date'})
        }




from django.contrib.auth.forms import PasswordChangeForm

class OptionalPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False  # 🔁 Treu el "required" HTML
            field.widget.attrs.pop('required', None)  # 🔁 Elimina l'atribut si existeix

    def is_filled(self):
        return all([
            self.cleaned_data.get('old_password'),
            self.cleaned_data.get('new_password1'),
            self.cleaned_data.get('new_password2'),
        ])

    def clean(self):
        cleaned_data = super().clean()
        if not self.is_filled():
            self._errors.clear()
        return cleaned_data

    def save(self, commit=True):
        if self.is_filled():
            return super().save(commit=commit)
        return self.user
