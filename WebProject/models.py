from users.models import User
from django.db import models

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Wallet {self.id}"


class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    datetime = models.DateTimeField()

    def __str__(self):
        return f"Transaction from Wallet {self.wallet.id} with amount {self.amount} on date: {self.datetime}"


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
