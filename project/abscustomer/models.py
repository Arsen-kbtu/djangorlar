from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.
class Customer1(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)


    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"