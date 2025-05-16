import logging
from functools import lru_cache
from typing import Any

from requests.exceptions import HTTPError

from users.models import User
from django.db import models

import yfinance as yf

logger = logging.getLogger(__name__)

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Wallet of {self.user.email} (balance of {self.balance} €)"


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
        ("STOCK", "Stock"),
        ("ETF", "Exchange-Traded-Fund"),
    ]

    type = models.CharField(max_length=6, choices=TYPES_OF_ASSETS_CHOICES)
    name = models.CharField(max_length=30)
    symbol = models.CharField(max_length=10)

    def __str__(self):
        return f"({self.type}) {self.symbol}"

    @staticmethod
    @lru_cache
    def __get_info(type: str, symbol: str) -> dict[str, Any]:
        if type == 'STOCK' or type == 'ETF':
            # Use the Yahoo! Finance API
            try:
                return yf.Ticker(symbol).info
            except HTTPError:
                logger.error(f'Failed to download data for {symbol}')
        raise NotImplemented

    @property
    def info(self) -> dict[str, Any]:
        return Asset.__get_info(self.type, self.symbol)

    @property
    def price(self) -> float:
        return self.price_history()[0]

    def price_history(self, period: int = 1) -> list[float]:
        return yf.Ticker(self.symbol).history(period=f'{period}d', prepost=True)['Close'].tolist()

    @property
    def stock_change(self) -> float:
        return (self.info.get('currentPrice') / self.info.get('previousClose')) - 1

class Holding(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Wallet {self.user.email} => {self.asset.name} = {self.amount}"
