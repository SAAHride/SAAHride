from django import forms
from .models import Driver, RideRequest

class DriverRegistrationForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['phone', 'car_type', 'plate_number']


class RideRequestForm(forms.ModelForm):
    class Meta:
        model = RideRequest
        fields = ['destination', 'ride_type']  # remove pickup_location
        widgets = {
            'destination': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Where are you going?'}),
            'ride_type': forms.Select(choices=[
                ('Economy', 'Economy'),
                ('Standard', 'Standard'),
                ('VIP', 'VIP'),
                ('VVIP', 'VVIP')
            ], attrs={'class': 'form-control'}),
        }