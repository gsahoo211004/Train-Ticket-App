from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking, Train
from .forms import TrainSearchForm
import datetime
from decimal import Decimal
from wallet.models import Wallet, PaymentSource

@login_required(login_url='login')
def bookings_view(request):
    bookings = Booking.objects.filter(
        user=request.user
    ).order_by('-booked_at')
    return render(request, 'bookings/bookings.html', {'bookings': bookings})

@login_required(login_url='login')
def booking_detail_view(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id, user=request.user)
    except Booking.DoesNotExist:
        return redirect('bookings')
    return render(request, 'bookings/booking_detail.html', {'booking': booking})

@login_required(login_url='login')
def search_trains_view(request):
    form = TrainSearchForm(request.GET or None)
    trains = []
    searched = False

    if request.GET and form.is_valid():
        searched = True
        source = form.cleaned_data['source'].strip().title()
        destination = form.cleaned_data['destination'].strip().title()
        journey_date = form.cleaned_data['journey_date']
        travel_class = form.cleaned_data['travel_class']
        passengers = form.cleaned_data['passengers']

        # Get day of week for the journey date
        day_map = {0:'Mon', 1:'Tue', 2:'Wed', 3:'Thu', 4:'Fri', 5:'Sat', 6:'Sun'}
        journey_day = day_map[journey_date.weekday()]

        # Filter trains
        qs = Train.objects.filter(
            source__icontains=source,
            destination__icontains=destination,
            available_seats__gte=passengers
        )
        if travel_class:
            qs = qs.filter(travel_class=travel_class)

        # Filter by day availability
        trains = [t for t in qs if journey_day in t.days_available.split(',')]

        if not trains:
            messages.error(request, f"No trains found from {source} to {destination} on {journey_date}.")

    return render(request, 'bookings/search_trains.html', {
        'form': form,
        'trains': trains,
        'searched': searched,
        'journey_date': request.GET.get('journey_date', ''),
        'passengers': request.GET.get('passengers', 1),
    })

@login_required(login_url='login')
def book_train_view(request, train_id):
    try:
        train = Train.objects.get(id=train_id)
    except Train.DoesNotExist:
        messages.error(request, "Train not found.")
        return redirect('search_trains')

    journey_date_str = request.GET.get('date') or request.POST.get('journey_date')
    passengers = int(request.GET.get('passengers', 1) or request.POST.get('passengers', 1))

    try:
        journey_date = datetime.date.fromisoformat(journey_date_str)
    except (ValueError, TypeError):
        messages.error(request, "Invalid journey date.")
        return redirect('search_trains')

    total_fare = train.fare_per_person * Decimal(passengers)
    wallet, _ = Wallet.objects.get_or_create(user=request.user)
    saved_sources = PaymentSource.objects.filter(user=request.user)

    # Partial payment calculation
    wallet_contribution = min(wallet.balance, total_fare)
    remaining = total_fare - wallet_contribution
    use_partial = wallet.balance > 0 and wallet.balance < total_fare

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        use_wallet_partial = request.POST.get('use_wallet_partial') == 'on'

        # Check seat availability
        if train.available_seats < passengers:
            messages.error(request, "Not enough seats available.")
            return redirect('search_trains')

        # Payment logic
        if payment_method == 'wallet':
            if wallet.balance < total_fare:
                messages.error(
                    request,
                    f"Insufficient wallet balance. "
                    f"Your balance: ₹{wallet.balance}. Required: ₹{total_fare}."
                )
                return render(request, 'bookings/book_train.html', {
                    'train': train,
                    'journey_date': journey_date,
                    'passengers': passengers,
                    'total_fare': total_fare,
                    'wallet': wallet,
                    'saved_sources': saved_sources,
                    'use_partial': use_partial,
                    'wallet_contribution': wallet_contribution,
                    'remaining': remaining,
                })
            wallet.balance -= total_fare
            wallet.save()

        elif use_wallet_partial and payment_method in ['savings', 'credit']:
            # Partial: use all wallet balance + rest from other source
            wallet.balance = 0
            wallet.save()
            # Remaining charged to savings/credit (assumed successful)

        # else: full payment from savings/credit

        # Create booking
        booking = Booking.objects.create(
            user=request.user,
            train=train,
            train_name=train.train_name,
            train_number=train.train_number,
            source=train.source,
            destination=train.destination,
            journey_date=journey_date,
            journey_time=train.departure_time,
            passengers=passengers,
            total_fare=total_fare,
            travel_class=train.travel_class,
            payment_method=payment_method,
            status='confirmed'
        )

        # Reduce seats
        train.available_seats -= passengers
        train.save()

        messages.success(request, f"Booking confirmed! Booking ID: #{booking.id}")
        return redirect('booking_confirmation', booking_id=booking.id)

    return render(request, 'bookings/book_train.html', {
        'train': train,
        'journey_date': journey_date,
        'passengers': passengers,
        'total_fare': total_fare,
        'wallet': wallet,
        'saved_sources': saved_sources,
        'use_partial': use_partial,
        'wallet_contribution': wallet_contribution,
        'remaining': remaining,
    })

@login_required(login_url='login')
def booking_confirmation_view(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id, user=request.user)
    except Booking.DoesNotExist:
        return redirect('bookings')
    return render(request, 'bookings/booking_confirmation.html', {'booking': booking})

@login_required(login_url='login')
def cancel_booking_view(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id, user=request.user)
    except Booking.DoesNotExist:
        messages.error(request, "Booking not found.")
        return redirect('bookings')

    if booking.status == 'cancelled':
        messages.error(request, "This booking is already cancelled.")
        return redirect('booking_detail', booking_id=booking.id)

    if request.method == 'POST':
        # Refund to wallet
        wallet, _ = Wallet.objects.get_or_create(user=request.user)
        wallet.balance += booking.total_fare
        wallet.save()

        # Restore seats
        if booking.train:
            booking.train.available_seats += booking.passengers
            booking.train.save()

        # Cancel booking
        booking.status = 'cancelled'
        booking.save()

        messages.success(
            request,
            f"Booking #{booking.id} cancelled. ₹{booking.total_fare} refunded to your wallet."
        )
        return redirect('bookings')

    return render(request, 'bookings/cancel_booking.html', {'booking': booking})


@login_required(login_url='login')
def change_date_view(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id, user=request.user)
    except Booking.DoesNotExist:
        messages.error(request, "Booking not found.")
        return redirect('bookings')

    if booking.status == 'cancelled':
        messages.error(request, "Cannot change date on a cancelled booking.")
        return redirect('booking_detail', booking_id=booking.id)

    if request.method == 'POST':
        new_date_str = request.POST.get('new_date')

        try:
            new_date = datetime.date.fromisoformat(new_date_str)
        except (ValueError, TypeError):
            messages.error(request, "Invalid date selected.")
            return redirect('change_date', booking_id=booking.id)

        if new_date < datetime.date.today():
            messages.error(request, "New date cannot be in the past.")
            return redirect('change_date', booking_id=booking.id)

        if new_date == booking.journey_date:
            messages.error(request, "New date is the same as the current date.")
            return redirect('change_date', booking_id=booking.id)

        # Check day availability for the train
        if booking.train:
            day_map = {0:'Mon', 1:'Tue', 2:'Wed', 3:'Thu', 4:'Fri', 5:'Sat', 6:'Sun'}
            new_day = day_map[new_date.weekday()]
            if new_day not in booking.train.days_available.split(','):
                messages.error(
                    request,
                    f"Train {booking.train_name} does not run on "
                    f"{new_date.strftime('%A')}s. "
                    f"Available days: {booking.train.days_available}"
                )
                return redirect('change_date', booking_id=booking.id)

        old_date = booking.journey_date
        booking.journey_date = new_date
        booking.save()

        messages.success(
            request,
            f"Journey date changed from {old_date} to {new_date} successfully!"
        )
        return redirect('booking_detail', booking_id=booking.id)

    return render(request, 'bookings/change_date.html', {'booking': booking,'today': datetime.date.today(),})

@login_required(login_url='login')
def feedback_view(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id, user=request.user)
    except Booking.DoesNotExist:
        return redirect('bookings')

    # Check if feedback already submitted
    if hasattr(booking, 'feedback'):
        messages.info(request, "You have already submitted feedback for this booking.")
        return redirect('booking_detail', booking_id=booking.id)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '')

        if not rating:
            messages.error(request, "Please select a rating.")
            return render(request, 'bookings/feedback.html', {'booking': booking})

        from .models import Feedback
        Feedback.objects.create(
            booking=booking,
            user=request.user,
            rating=int(rating),
            comment=comment
        )
        messages.success(request, "Thank you for your feedback! 🌟")
        return redirect('booking_detail', booking_id=booking.id)

    return render(request, 'bookings/feedback.html', {'booking': booking})