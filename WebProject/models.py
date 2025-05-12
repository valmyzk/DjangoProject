from users.models import User
from django.db import models

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Wallet of {self.user.email} (balance of {self.balance}€)"


class Transaction(models.Model):
    source = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transaction_source')
    destination = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transaction_destination')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    datetime = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f"Transaction from {self.source.user.email} to {self.destination.user.email} with amount {self.amount} on date: {self.datetime}"


class Asset(models.Model):
    TYPES_OF_ASSETS_CHOICES = [
        ("CRYPTO", "Cryptocurrency"),
        ("STK", "Stock"),
        ("ETF", "Exchange-Traded Fund"),
    ]
    type = models.CharField(max_length=6, choices=TYPES_OF_ASSETS_CHOICES)
    name = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"({self.type}) {self.name}: {self.price} EUR"


class Holding(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Wallet {self.wallet.id} => {self.asset.name} = {self.amount}"
