from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from WebProject.models import Transaction, Wallet
from users.models import User

BOOTSTRAP_ATTRS = {'class': 'form-control bg-dark text-white border-secondary'}

class EditProfileForm(forms.Form):
    """
    Form used to partially update contents of the user model.
    """
    email = forms.CharField(disabled=True, widget=forms.EmailInput(BOOTSTRAP_ATTRS))
    phone = forms.CharField(widget=forms.TelInput(BOOTSTRAP_ATTRS))
    date_of_birth = forms.CharField(widget=forms.DateInput(BOOTSTRAP_ATTRS | {'type': 'date'}))

class AddFundsForm(forms.Form):
    """
    Form used to add funds to a wallet. (Free money!)
    """
    amount = forms.DecimalField(label='Amount:', min_value=0, decimal_places=2, step_size=0.1, widget=forms.NumberInput(BOOTSTRAP_ATTRS))

class TransferFundsForm(forms.Form):
    """
    Form used to transfer funds from one account to the other.
    """
    destination = forms.CharField(label=_('Account to transfer funds into:'), required=True, widget=forms.TextInput(BOOTSTRAP_ATTRS))
    amount = forms.DecimalField(label=_('Amount to transfer:'), required=True, min_value=0, step_size=0.1, widget=forms.NumberInput(BOOTSTRAP_ATTRS))

    def __init__(self, user: User, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_destination(self):
        """
        Ensures the destination wallet exists and isn't your own.
        """
        try:
            self.wallet = Wallet.objects.get(user__email=self.cleaned_data['destination'])
        except Wallet.DoesNotExist:
            raise ValidationError('Invalid destination account', code='invalid')
        if self.wallet.pk == self.user.wallet.pk:
            raise ValidationError("Can't transfer to your own account", code='invalid')
        return self.cleaned_data['destination']

    def clean_amount(self):
        """
        Ensures the user's wallet has enough balance to perform the transfer.
        :return:
        """
        if self.user.wallet.balance < self.cleaned_data['amount']:
            raise ValidationError('Not enough balance in your wallet', code='balance')
        return self.cleaned_data['amount']
