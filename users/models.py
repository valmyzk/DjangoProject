from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=200, unique=True)