from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = [
        ('user', 'Regular User'),
        ('admin', 'Admin'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    phone = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    id_proof = models.FileField(upload_to='id_proofs/', blank=True, null=True)
    address_proof = models.FileField(upload_to='address_proofs/', blank=True, null=True)
    kyc_verified = models.BooleanField(default=False)
    kyc_pending = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.role}"