from django.db import models
from site_auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    photo = models.ImageField(upload_to='products', null=True)
    description = models.TextField(max_length=300, null=True)
    price = models.IntegerField(null=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, null=True)

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
    accepted = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'order {self.id}'


class Banner(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    photo = models.ImageField(upload_to='banners')

    def __str__(self):
        return self.name if self.name else f'banner {self.id}'


class Filial(models.Model):
    name = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    open_times = models.CharField(max_length=200, null=True)
    phone_number = models.CharField(max_length=20, null=True)
    orienter = models.CharField(max_length=200, null=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
