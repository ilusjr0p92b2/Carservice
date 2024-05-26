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
        return f'{self.brand} {self.model} {self.year}'

    class Meta:
        verbose_name = 'Машина'
        verbose_name_plural = 'Машины'


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='services')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_orders')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, blank=True)
    services = models.ManyToManyField(Service)
    date = models.DateField()
    time = models.TimeField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user}-{self.date}-{self.time}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
