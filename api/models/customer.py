from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=14, null=True, blank=True)
    country = models.CharField(max_length=3, null=True, blank=True)
    address = models.TextField(max_length=512)
    phone = models.CharField(max_length=50)
