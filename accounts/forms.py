from django import forms
from django.contrib.auth.models import User
from .models import Driver, RideRequest, Profile

# === Custom User Registration Form with Phone Number ===
class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    phone_number = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            # Save phone and verification code into the Profile
            profile = user.profile
            profile.phone_number = self.cleaned_data['phone_number']
            profile.verification_code = '123456'  # Temporary until SMS/email is implemented
            profile.save()
        return user

# === Driver Registration ===
class DriverRegistrationForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['phone', 'car_type', 'plate_number']

# === Ride Request ===
class RideRequestForm(forms.ModelForm):
    class Meta:
        model = RideRequest
        fields = ['destination', 'ride_type']  # pickup_location removed, handled automatically
        widgets = {
            'destination': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Where are you going?'
            }),
            'ride_type': forms.Select(choices=[
                ('Economy', 'Economy'),
                ('Standard', 'Standard'),
                ('VIP', 'VIP'),
                ('VVIP', 'VVIP')
            ], attrs={'class': 'form-control'}),
        }