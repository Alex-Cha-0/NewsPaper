from django.db import models
from datetime import datetime
from django.core.validators import MinValueValidator


class Product(models.Model):
    DRINK = 'DRNK'
    BURGER = 'BRGR'
    SNACK = 'SNCK'
    DESSERT = 'DSRT'

    TYPE_CHOICES = [
        (DRINK, 'Drink'),
        (BURGER, 'Burger'),
        (SNACK, 'Snack'),
        (DESSERT, 'Dessert'),
    ]
    type = models.CharField(max_length=5, choices=TYPE_CHOICES, default=BURGER)
    name = models.CharField(
        max_length=255,
        unique=True
    )
    price = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
    )
    description = models.TextField()

    category = models.ForeignKey(to='Category', on_delete=models.CASCADE, related_name='products', null=True)

    def __str__(self):
        return f'Product #{self.name} - Описание: {self.description[:20]}'

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром
        return f'/products/product/{self.id}'


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f'{self.name.title()}'
