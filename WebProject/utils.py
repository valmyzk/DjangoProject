import logging
from decimal import Decimal

from django.db import transaction

from WebProject.models import Wallet, Transaction
from users.models import User

logger = logging.getLogger(__name__)

def transfer_funds_internal(source: Wallet, destination: Wallet, amount: Decimal) -> None:
    """
    Registers a transaction.
    """
    with transaction.atomic():
        source.balance -= amount
        destination.balance += amount
        source.save()
        destination.save()
        Transaction.objects.create(source=source, destination=destination, amount=amount)
    logger.info(f'Transferred {amount}€ from {source.user.email} to {destination.user.email}')

def get_admin() -> User:
    """
    :return: the administrator's account.
    """
    return User.objects.get(email='admin@admin.com')