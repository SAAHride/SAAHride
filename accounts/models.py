from django.db import models
from django.contrib.auth.models import User


class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    car_type = models.CharField(max_length=50)
    plate_number = models.CharField(max_length=20)

    def _str_(self):
        return f"{self.user.username} - {self.car_type} ({self.plate_number})"


class RideRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pickup_location = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    ride_type = models.CharField(max_length=50, blank=True)  # e.g., regular, premium
    requested_at = models.DateTimeField(auto_now_add=True)
    accepted_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='accepted_rides'
    )

    def _str_(self):
        return f"{self.user.username} - {self.pickup_location} to {self.destination}"


# ✅ Add Profile for phone verification
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def _str_(self):
        return self.user.username