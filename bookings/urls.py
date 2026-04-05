from django.urls import path
from . import views

urlpatterns = [
    path('', views.bookings_view, name='bookings'),
    path('search/', views.search_trains_view, name='search_trains'),
    path('book/<int:train_id>/', views.book_train_view, name='book_train'),
    path('confirmation/<int:booking_id>/', views.booking_confirmation_view, name='booking_confirmation'),
    path('<int:booking_id>/', views.booking_detail_view, name='booking_detail'),
    path('<int:booking_id>/cancel/', views.cancel_booking_view, name='cancel_booking'),
    path('<int:booking_id>/change-date/', views.change_date_view, name='change_date'),
    path('<int:booking_id>/feedback/', views.feedback_view, name='feedback'),
]