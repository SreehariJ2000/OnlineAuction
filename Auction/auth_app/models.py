from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN="ADMIN",'Admin'
        CUSTOMER="CUSTOMER",'Customer'
        SELLER="SELLER",'Seller'
        SERVICE="SERVICE",'Service'


    role = models.CharField(max_length=50,choices=Role.choices)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=12, unique=True)  # You can adjust the max_length as needed
    bidder_id = models.CharField(max_length=10, unique=True)  # You can adjust the max_length as needed

    def __str__(self):
        return self.user.username