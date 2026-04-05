from django.contrib import admin
from .models import Booking, Train, Feedback

admin.site.register(Booking)
admin.site.register(Train)
admin.site.register(Feedback)