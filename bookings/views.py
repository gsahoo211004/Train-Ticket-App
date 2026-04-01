from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Booking

@login_required(login_url='login')
def bookings_view(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booked_at')
    return render(request, 'bookings/bookings.html', {'bookings': bookings})

@login_required(login_url='login')
def booking_detail_view(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id, user=request.user)
    except Booking.DoesNotExist:
        return redirect('bookings')
    return render(request, 'bookings/booking_detail.html', {'booking': booking})