from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm as BaseUserCreationForm, UserChangeForm as BaseUserChangeForm
from .models import User

BOOTSTRAP_ATTRS = {'class': 'form-control bg-dark text-white border-secondary'}

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'phone', 'date_of_birth', 'profile_picture')
        widgets = {
            'email': forms.EmailInput(BOOTSTRAP_ATTRS),
            'phone': forms.TextInput(BOOTSTRAP_ATTRS | {'type': 'tel'}),
            'date_of_birth': forms.DateInput(BOOTSTRAP_ATTRS | {'type': 'date'}),
        }

    profile_picture = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Current password',
        widget=forms.PasswordInput(BOOTSTRAP_ATTRS),
        required=False
    )
    new_password1 = forms.CharField(
        label='New password',
        widget=forms.PasswordInput(BOOTSTRAP_ATTRS),
        required=False
    )
    new_password2 = forms.CharField(
        label='Confirm new password',
        widget=forms.PasswordInput(BOOTSTRAP_ATTRS),
        required=False
    )

    def clean(self):
        cleaned_data = super().clean()

        # Omplert algun camp → validar normal
        if any([
            cleaned_data.get('old_password'),
            cleaned_data.get('new_password1'),
            cleaned_data.get('new_password2')
        ]):
            return super().clean()

        # Cap camp omplert → evitar validació i no actualitzar contrasenya
        self.cleaned_data.clear()
        return cleaned_data

class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'phone', 'date_of_birth', 'profile_picture')

class UserChangeForm(BaseUserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'phone', 'date_of_birth', 'profile_picture')
