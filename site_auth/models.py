from django.db import models
from django.contrib.auth.models import AbstractUser
from random import randint
from datetime import datetime, timedelta


class User(AbstractUser):
    address = models.ForeignKey('api.Address', on_delete=models.SET_NULL, null=True, blank=True)


class SMSCode(models.Model):
    phone_number = models.CharField(max_length=20, null=True)
    code = models.IntegerField(null=True, unique=True)
    expiration_date = models.DateTimeField(null=True, default=datetime.today() + timedelta(minutes=2))

    def __str__(self):
        return f'{self.phone_number}'

    def is_expired(self):
        today = datetime.today()
        if self.expiration_date:
            if self.expiration_date >= today:
                return False
            else:
                return True
        else:
            return True
