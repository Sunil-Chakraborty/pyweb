# transactions/models.py

from django.db import models

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('Rct', 'Receipt'),
        ('Exp', 'Payment'),
    ]

    tr = models.CharField(max_length=3, choices=TRANSACTION_TYPES)
    name = models.CharField(max_length=255)
    comment = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.tr} - Rs.{self.amount}"
