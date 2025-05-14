import logging
from decimal import Decimal
from datetime import date

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
    admin, created = User.objects.get_or_create(
        email='admin@admin.com',
        defaults={
            'password': 'admin',  # Default password
            'phone': '999 999 999',
            'date_of_birth': '1970-01-01',
            'is_staff': True,
            'is_superuser': True
        }
    )

    # Set the password if the user was created or if password is None
    if created or admin.password is None:
        admin.set_password('admin')
        admin.save()


    return admin