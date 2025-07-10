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

    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        self.fields['pickup_location'].required = False  # let JavaScript fill it
        