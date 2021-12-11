from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone_number = models.CharField(max_length=12, null=True)
    address = models.ForeignKey('api.Address', on_delete=models.SET_NULL, null=True)
