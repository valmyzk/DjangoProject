import logging
from decimal import Decimal

from django.db import transaction


from WebProject.models import Wallet, Transaction, Holding, Asset
from users.models import User

logger = logging.getLogger(__name__)



def transfer_funds_internal(source: Wallet, destination: Wallet, amount: Decimal) -> Transaction:
    """
    Registers a transaction and returns it.
    """
    with transaction.atomic():
        source.balance -= amount
        destination.balance += amount
        source.save()
        destination.save()
        transfer = Transaction.objects.create(source=source, destination=destination, amount=amount)
    logger.info(f'Transferred {amount}€ from {source.user.email} to {destination.user.email}')
    return transfer


def add_funds_to_holding(user: User, asset: Asset, amount: Decimal):
    """
    Adds an amount to a holding, or creates it if it doesn't exist.
    """
    holding, _ = Holding.objects.get_or_create(user=user, asset=asset)
    holding.amount += amount
    holding.save()


def get_admin() -> User:
    """
    :return: the administrator's account.
    """
    admin = User.objects.get(email='admin@admin.com')
    return admin


def subtract_funds_from_holding(user, asset, amount):
    """
    Substracts amount from the holding. If holding amount is 0, the holding is deleted.
    """
    holding = Holding.objects.get(user=user, asset=asset)
    holding.amount -= amount
    if holding.amount <= 0:
        holding.delete()
    else:
        holding.save()
