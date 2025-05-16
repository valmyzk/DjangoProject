from decimal import Decimal

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from WebProject.models import Wallet, Asset, Holding
from users.models import User

BOOTSTRAP_ATTRS = {'class': 'form-control bg-dark text-white border-secondary'}

class EditProfileForm(forms.Form):
    """
    Form used to partially update contents of the user model.
    """
    email = forms.CharField(disabled=True, widget=forms.EmailInput(BOOTSTRAP_ATTRS))
    phone = forms.CharField(widget=forms.TextInput(BOOTSTRAP_ATTRS | {'type': 'tel'}))
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

class BuyAnAssetForm(forms.Form):
    """
    Form used to buy an asset.
    """
    asset = forms.CharField(label=_('Asset:'), required=True, widget=forms.TextInput(BOOTSTRAP_ATTRS))
    amount = forms.DecimalField(label='Amount:', min_value=0, decimal_places=2, step_size=0.1, widget=forms.NumberInput(BOOTSTRAP_ATTRS))
    
    def __init__(self, user: User, *args, **kwargs):
        self.user = user
        self.price = 0
        super().__init__(*args, **kwargs)

    def clean(self):
        try:
            asset = Asset.objects.get(symbol=self.cleaned_data['asset'])
        except Asset.DoesNotExist:
            raise ValidationError('Invalid asset symbol', code='invalid')
        self.price = Decimal(asset.price) * self.cleaned_data['amount']
        if self.user.wallet.balance < self.price:
            raise ValidationError('Not enough balance', code='balance')
        return {'asset': asset, 'amount': self.cleaned_data['amount']}

class SellAnAssetForm(forms.Form):
    asset = forms.ChoiceField(
        label=_('Asset'),
        required=True,
        widget=forms.Select(BOOTSTRAP_ATTRS)
    )
    amount = forms.DecimalField(
        label=_('Amount'),
        required=True,
        min_value=Decimal('0.01'),
        decimal_places=2,
        max_digits=10,
        widget=forms.NumberInput(BOOTSTRAP_ATTRS)
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        self.asset_instance = None
        self.price = Decimal('0')
        super().__init__(*args, **kwargs)

        owned_assets = Holding.objects.filter(user=user).select_related('asset')
        self.choices_map = {str(h.asset.symbol): h.asset for h in owned_assets}
        self.fields['asset'].choices = [(symbol, f"{asset.name} ({symbol})") for symbol, asset in self.choices_map.items()]

    def clean(self):
        cleaned_data = super().clean()
        symbol = cleaned_data.get('asset')
        amount = cleaned_data.get('amount')

        if symbol not in self.choices_map:
            raise ValidationError(_('Invalid asset or you do not own it.'), code='invalid_asset')

        self.asset_instance = self.choices_map[symbol]

        try:
            holding = Holding.objects.get(user=self.user, asset=self.asset_instance)
        except Holding.DoesNotExist:
            raise ValidationError(_('You do not own this asset.'), code='no_holding')

        if holding.amount < amount:
            raise ValidationError(_('You do not have enough of this asset to sell.'), code='insufficient_amount')

        self.price = Decimal(str(self.asset_instance.price))* amount
        return cleaned_data