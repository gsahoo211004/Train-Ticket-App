from django import forms
from datetime import date

class TrainSearchForm(forms.Form):
    CLASS_CHOICES = [
        ('', 'Any Class'),
        ('SL', 'Sleeper'),
        ('3A', 'AC 3 Tier'),
        ('2A', 'AC 2 Tier'),
        ('1A', 'AC First Class'),
    ]
    source = forms.CharField(max_length=100, label='From')
    destination = forms.CharField(max_length=100, label='To')
    journey_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Journey Date'
    )
    travel_class = forms.ChoiceField(choices=CLASS_CHOICES, required=False, label='Class')
    passengers = forms.IntegerField(min_value=1, max_value=6, initial=1, label='Passengers')

    def clean_journey_date(self):
        d = self.cleaned_data['journey_date']
        if d < date.today():
            raise forms.ValidationError("Journey date cannot be in the past.")
        return d
    
class BookingForm(forms.Form):
    passengers = forms.IntegerField(min_value=1, max_value=6, label='Number of Passengers')
    journey_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Journey Date'
    )
    payment_method = forms.ChoiceField(
        choices=[
            ('wallet', 'Wallet Balance'),
            ('savings', 'Savings Account'),
            ('credit', 'Credit Card'),
        ],
        label='Payment Method'
    )

    def clean_journey_date(self):
        d = self.cleaned_data['journey_date']
        if d < date.today():
            raise forms.ValidationError("Journey date cannot be in the past.")
        return d