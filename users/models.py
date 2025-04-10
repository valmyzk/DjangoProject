from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    email = models.EmailField(max_length=200, unique=True)
    phone = models.CharField(max_length=15)
    country = CountryField()
    address = models.CharField(max_length=50)
    date_of_birth = models.DateField()
