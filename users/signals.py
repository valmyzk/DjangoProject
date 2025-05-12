from django.db.models.signals import post_save
from django.dispatch import receiver
from WebProject.models import Wallet
from .models import User

@receiver(post_save, sender=User)
def create_wallet_for_new_user(sender: type[User], instance: User, created: bool, **kwargs):
    if created:
        Wallet.objects.create(user=instance)
