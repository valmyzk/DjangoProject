from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import uuid

class UserManager(BaseUserManager):
    """
    Custom user model manager.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractUser):
    """
    Custom user model which holds additional data.
    """
    username = None
    email = models.EmailField(_('email address'), unique=True, null=False)
    phone = models.CharField(_('phone number'), max_length=15, null=False)
    date_of_birth = models.DateField(_('date of birth'), null=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()