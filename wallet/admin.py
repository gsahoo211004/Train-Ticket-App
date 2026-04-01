from django.contrib import admin
from .models import Wallet, PaymentSource
admin.site.register(Wallet)
admin.site.register(PaymentSource)