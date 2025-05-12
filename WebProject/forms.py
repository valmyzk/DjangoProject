from django import forms

BOOTSTRAP_ATTRS = {'class': 'form-control bg-dark text-white border-secondary'}

class EditProfileForm(forms.Form):
    """
    Form used to partially update contents of the user model.
    """
    email = forms.CharField(disabled=True, widget=forms.EmailInput(BOOTSTRAP_ATTRS))
    phone = forms.CharField(widget=forms.TelInput(BOOTSTRAP_ATTRS))
    date_of_birth = forms.CharField(widget=forms.DateInput(BOOTSTRAP_ATTRS | {'type': 'date'}))