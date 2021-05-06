from django.db import models

from .order import Order


class Invoice(models.Model):
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    issued = models.DateTimeField(null=True, blank=True)
    due = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    # def to_dict(self):
    #     return {
    #         "id": self.id,
    #         "issued": self.issued,
    #         "due": self.due,
    #         "amount": self.amount
    #     }


class Payment(models.Model):
    name = models.CharField(max_length=128, null=True)
    amount = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)