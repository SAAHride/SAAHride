# accounts/views.py
from django.core.mail import send_mail
from .models import Profile
from django.shortcuts import render



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
            return redirect('ride_status', ride_id=ride.id)
    else:
        form = RideRequestForm()
    return render(request, 'accounts/request_ride.html', {'form': form})


# ========== Driver Dashboard ==========

@login_required
def driver_dashboard(request):
    pending_rides = RideRequest.objects.filter(status='Pending')
    return render(request, 'accounts/driver_dashboard.html', {'pending_rides': pending_rides})


@login_required
def accept_ride(request, ride_id):
    ride = get_object_or_404(RideRequest, id=ride_id)
    if ride.status == 'Pending':
        ride.status = 'Accepted'
        ride.accepted_by = request.user
        ride.save()
    return redirect('driver_dashboard')

@login_required
def start_ride(request, ride_id):
    ride = get_object_or_404(RideRequest, id=ride_id, accepted_by=request.user)
    if ride.status == 'Accepted':
        ride.status = 'In Progress'
        ride.save()
    return redirect('driver_dashboard')


@login_required
def complete_ride(request, ride_id):
    ride = get_object_or_404(RideRequest, id=ride_id, accepted_by=request.user)
    if ride.status == 'In Progress':
        ride.status = 'Completed'
        ride.save()
    return redirect('driver_dashboard')

@login_required
def ride_status_view(request, ride_id):
    ride = get_object_or_404(RideRequest, id=ride_id, user=request.user)
    return render(request, 'accounts/ride_status.html', {
        'ride': ride
    })
def is_driver(user):
    return hasattr(user, 'driver')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            code = user.profile.verification_code
            send_mail(
                'SAAHride Verification Code',
                f'Your code is: {code}',
                'noreply@saahride.com',
                [user.email],
                fail_silently=False
            )
            return redirect('verify_code')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def verify_code_view(request):
    return render(request, 'accounts/verify_code.html')  # Make sure this template exists
    if request.method == 'POST':
        code = request.POST.get('code')
        profile = request.user.profile
        if profile.verification_code == code:
            profile.is_verified = True
            profile.save()
            return redirect('dashboard')
    return render(request, 'registration/verify.html')
    return render(request, 'accounts/verify_code.html')  # Make sure this template exists