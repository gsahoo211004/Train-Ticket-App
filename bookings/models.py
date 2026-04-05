from django.db import models
from django.contrib.auth.models import User

class Train(models.Model):
    CLASS_CHOICES = [
        ('SL', 'Sleeper'),
        ('3A', 'AC 3 Tier'),
        ('2A', 'AC 2 Tier'),
        ('1A', 'AC First Class'),
    ]
    train_number = models.CharField(max_length=10, unique=True)
    train_name = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    total_seats = models.PositiveIntegerField(default=100)
    available_seats = models.PositiveIntegerField(default=100)
    fare_per_person = models.DecimalField(max_digits=8, decimal_places=2)
    travel_class = models.CharField(max_length=5, choices=CLASS_CHOICES, default='SL')
    days_available = models.CharField(
        max_length=50,
        default='Mon,Tue,Wed,Thu,Fri,Sat,Sun',
        help_text='Comma-separated days e.g. Mon,Wed,Fri'
    )

    def __str__(self):
        return f"{self.train_number} - {self.train_name} ({self.source} to {self.destination})"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('pending', 'Pending'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    train = models.ForeignKey(Train, on_delete=models.SET_NULL, null=True, blank=True)
    train_name = models.CharField(max_length=100)
    train_number = models.CharField(max_length=20)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    journey_date = models.DateField()
    journey_time = models.TimeField()
    passengers = models.PositiveIntegerField(default=1)
    total_fare = models.DecimalField(max_digits=8, decimal_places=2)
    travel_class = models.CharField(max_length=5, default='SL')
    payment_method = models.CharField(max_length=20, default='wallet')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='confirmed')
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.train_name} ({self.journey_date})"

class Feedback(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.user.username} for Booking #{self.booking.id}"