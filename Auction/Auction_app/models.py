
from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from auth_app.models import SellerProfile



class Category(models.Model):
    cat_name = models.CharField(max_length=100)

    def __str__(self):
        return self.cat_name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_name = models.CharField(max_length=100)

    def __str__(self):
        return self.sub_name
    

class AddProduct(models.Model):
    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE)
    category =  models.CharField(max_length=100)
    sub_category = models.CharField(max_length=100)
    product_name = models.CharField(max_length=255)
    tags = models.CharField(max_length=255)
    about_product = RichTextField()
    auction_start_datetime = models.DateTimeField(default=timezone.now)
    auction_end_datetime = models.DateTimeField()
    image1 = models.ImageField(upload_to='products/')
    image2 = models.ImageField(upload_to='products/', blank=True, null=True)
    image3 = models.ImageField(upload_to='products/', blank=True, null=True)
    image4 = models.ImageField(upload_to='products/', blank=True, null=True)
    authentication_certificate = models.FileField(upload_to='certificates/')
    sold = models.BooleanField(default=False)
    is_live = models.BooleanField(default=False)
    admin_approval = models.BooleanField(default=False)
	
    
    def __str__(self):
        return self.product_name