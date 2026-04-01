from django.urls import path
from . import views

urlpatterns = [
    path('', views.bookings_view, name='bookings'),
    path('<int:booking_id>/', views.booking_detail_view, name='booking_detail'),
]