
# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    car_type = models.CharField(max_length=50)
    plate_number = models.CharField(max_length=20)

    def _str_(self):
        return f"{self.user.username} - {self.car_type} ({self.plate_number})"
