from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Info(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.IntegerField()
    category = models.ManyToManyField(Category, related_name='products')

    def __str__(self):
        return self.name


class Location(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)


class SubOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


class Order(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    suborders = models.ManyToManyField(SubOrder)

    def __str__(self):
        return f'order {self.id}'
