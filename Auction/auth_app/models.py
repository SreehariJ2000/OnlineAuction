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
    

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=10)
    pincode = models.PositiveIntegerField()
    locality = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    landmark = models.CharField(max_length=255, blank=True, null=True)
    alt_phone = models.CharField(max_length=10, blank=True, null=True)
    address_type = models.CharField(max_length=10, choices=[('home', 'Home'), ('work', 'Work')])
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    
    def __str__(self):
        return f"{self.name} - {self.address_type} Address"





class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)  
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    address = models.CharField(max_length=255)
    pin = models.CharField(max_length=10)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    gender = models.CharField(max_length=10,blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name
    

        
