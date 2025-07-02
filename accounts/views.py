# accounts/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

from .forms import RideRequestForm, DriverRegistrationForm
from .models import RideRequest

# ========== Auth Views ==========

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    return render(request, 'registration/dashboard.html')


def home_view(request):
    return render(request, 'registration/home.html')


# ========== Driver Registration ==========

@login_required
def driver_register_view(request):
    if request.method == 'POST':
        form = DriverRegistrationForm(request.POST)
        if form.is_valid():
            driver = form.save(commit=False)
            driver.user = request.user
            driver.save()
            return redirect('dashboard')
    else:
        form = DriverRegistrationForm()
    return render(request, 'registration/driver_register.html', {'form': form})


# ========== User Ride Request ==========

@login_required
def request_ride_view(request):
    if request.method == 'POST':
        form = RideRequestForm(request.POST)
        if form.is_valid():
            ride = form.save(commit=False)
            ride.user = request.user
            ride.status = 'Pending'
            ride.save()
            return render(request, 'account/ride_confirmation.html', {
                'pickup': ride.pickup_location,
                'destination': ride.destination,
                'ride_type': ride.ride_type,
            })
    else:
        form = RideRequestForm()
    return render(request, 'account/request_ride.html', {'form': form})


# ========== Driver Dashboard ==========

@login_required
def driver_dashboard(request):
    pending_rides = RideRequest.objects.filter(status='Pending')
    return render(request, 'account/driver_dashboard.html', {'pending_rides': pending_rides})


@login_required
def accept_ride(request, ride_id):
    ride = get_object_or_404(RideRequest, id=ride_id)
    if ride.status == 'Pending':
        ride.status = 'Accepted'
        ride.accepted_by = request.user
        ride.save()
    return redirect('driver_dashboard')