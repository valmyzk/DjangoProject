import logging
from decimal import Decimal
from functools import lru_cache
from typing import Any

import yfinance as yf
from django.db import models
from requests.exceptions import HTTPError

from users.models import User

logger = logging.getLogger(__name__)


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Wallet of {self.user.email} (balance of {self.balance} €)"


class Transaction(models.Model):
    TYPE_CHOICES = [
        ('TRANSFER', 'Transfer'),
        ('ADD_FUNDS', 'Add Funds'),
        ('BUY', 'Buy Asset'),
        ('SELL', 'Sell Asset'),
        ('SELF', 'Self Transfer'),
    ]

    source = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transaction_source')
    destination = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transaction_destination')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    datetime = models.DateTimeField(auto_now_add=True, editable=False)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.type} from {self.source.user.email} to {self.destination.user.email} ({self.amount}€ on {self.datetime})"

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

    @staticmethod
    @lru_cache
    def __get_price_history(type: str, symbol: str, period: int):
        if type == 'STOCK' or type == 'ETF':
            # Use the Yahoo! Finance API
            try:
                return yf.Ticker(symbol).history(period=f'{period}d')['Close'].tolist()
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
        return self.__get_price_history(self.type, self.symbol, period)

    @property
    def stock_change(self) -> float:
        return ((self.info.get('currentPrice', 0) / self.info.get('previousClose')) - 1) * 100


class Holding(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Wallet {self.user.email} => {self.asset.name} = {self.amount}"

    @property
    def value(self) -> float:
        return float(Decimal(self.asset.price) * self.amount)
