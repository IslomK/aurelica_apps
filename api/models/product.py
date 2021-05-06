from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=128, null=True, blank=True)


class Product(models.Model):
    name = models.CharField(max_length=10, null=False)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    description = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)

