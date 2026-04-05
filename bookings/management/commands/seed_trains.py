from django.core.management.base import BaseCommand
from bookings.models import Train

class Command(BaseCommand):
    help = 'Seed sample train data'

    def handle(self, *args, **kwargs):
        Train.objects.all().delete()

        trains = [
            {
                'train_number': '12001',
                'train_name': 'Shatabdi Express',
                'source': 'Chennai',
                'destination': 'Bangalore',
                'departure_time': '06:00',
                'arrival_time': '11:00',
                'total_seats': 100,
                'available_seats': 100,
                'fare_per_person': 850.00,
                'travel_class': 'SL',
                'days_available': 'Mon,Tue,Wed,Thu,Fri,Sat,Sun',
            },
            {
                'train_number': '12002',
                'train_name': 'Rajdhani Express',
                'source': 'Chennai',
                'destination': 'Delhi',
                'departure_time': '08:00',
                'arrival_time': '06:00',
                'total_seats': 150,
                'available_seats': 150,
                'fare_per_person': 2200.00,
                'travel_class': '2A',
                'days_available': 'Mon,Wed,Fri,Sun',
            },
            {
                'train_number': '12003',
                'train_name': 'Coromandel Express',
                'source': 'Chennai',
                'destination': 'Kolkata',
                'departure_time': '09:30',
                'arrival_time': '08:00',
                'total_seats': 200,
                'available_seats': 200,
                'fare_per_person': 1500.00,
                'travel_class': 'SL',
                'days_available': 'Tue,Thu,Sat',
            },
            {
                'train_number': '12004',
                'train_name': 'Brindavan Express',
                'source': 'Bangalore',
                'destination': 'Chennai',
                'departure_time': '07:15',
                'arrival_time': '12:15',
                'total_seats': 120,
                'available_seats': 120,
                'fare_per_person': 750.00,
                'travel_class': 'SL',
                'days_available': 'Mon,Tue,Wed,Thu,Fri,Sat,Sun',
            },
            {
                'train_number': '12005',
                'train_name': 'Tamil Nadu Express',
                'source': 'Delhi',
                'destination': 'Chennai',
                'departure_time': '22:30',
                'arrival_time': '07:45',
                'total_seats': 180,
                'available_seats': 180,
                'fare_per_person': 1800.00,
                'travel_class': '3A',
                'days_available': 'Mon,Wed,Fri,Sat',
            },
            {
                'train_number': '12006',
                'train_name': 'Mumbai Express',
                'source': 'Chennai',
                'destination': 'Mumbai',
                'departure_time': '11:45',
                'arrival_time': '09:30',
                'total_seats': 160,
                'available_seats': 160,
                'fare_per_person': 1950.00,
                'travel_class': '2A',
                'days_available': 'Tue,Thu,Sun',
            },
        ]

        for t in trains:
            Train.objects.create(**t)
            self.stdout.write(f"  Created: {t['train_name']}")

        self.stdout.write(self.style.SUCCESS(
            f'\nSuccessfully seeded {len(trains)} trains!'
        ))