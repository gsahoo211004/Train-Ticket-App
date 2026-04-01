from django.db import models
from django.contrib.auth.models import User

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - ₹{self.balance}"

class PaymentSource(models.Model):
    SOURCE_TYPES = [
        ('savings', 'Savings Account'),
        ('credit', 'Credit Card'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source_type = models.CharField(max_length=10, choices=SOURCE_TYPES)
    account_number = models.CharField(max_length=20)
    label = models.CharField(max_length=50, blank=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.source_type}"