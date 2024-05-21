from django.db import models
from django.db.models import CASCADE

from authapp.models import User


class Car(models.Model):
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    vin = models.CharField(max_length=17, unique=True)
    owner = models.ForeignKey(User, on_delete=CASCADE)

    def __str__(self):
        return f'{self.brand} {self.model} ({self.year})'


class Service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Order(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    services = models.ManyToManyField(Service)
    date = models.DateField()
    time = models.TimeField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f'Order for {self.car} on {self.date} at {self.time}'
