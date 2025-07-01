from django import forms
from .models import Driver

class DriverRegistrationForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['phone', 'car_type', 'plate_number']