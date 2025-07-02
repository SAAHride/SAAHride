from django import forms
from .models import Driver, RideRequest

class DriverRegistrationForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['phone', 'car_type', 'plate_number']


class RideRequestForm(forms.ModelForm):
    class Meta:
        model = RideRequest
        fields = ['pickup_location', 'destination', 'ride_type']
        widgets = {
            'pickup_location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter pickup location'
            }),
            'destination': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter destination'
            }),
            'ride_type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Regular, Premium'
            }),
        }