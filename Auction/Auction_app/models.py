
from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from auth_app.models import *
from django.contrib.auth import get_user_model
User = get_user_model()




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
    current_price=models.IntegerField(default=0.0)
    current_highest_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)


    def total_sales(self):
        return ProductSale.objects.filter(product=self).aggregate(total_sales=models.Sum('sale_amount'))['total_sales'] or 0.0
    

	
    
    def __str__(self):
        return self.product_name
    

class Bid(models.Model):
    product = models.ForeignKey(AddProduct, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.product.product_name


class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    is_paid=models.BooleanField(default=False)


class CartItems(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    product=models.ForeignKey(AddProduct,on_delete=models.CASCADE)
    



class RejectedProduct(models.Model):
    product = models.ForeignKey(AddProduct, on_delete=models.CASCADE)
    reauction=models.BooleanField(default=False)

    def __str__(self):
        return self.product.product_name



class ProductSale(models.Model):
    product = models.ForeignKey(AddProduct, on_delete=models.CASCADE)
    sale_amount = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.product.product_name} - {self.sale_date}"


class UserPayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    cart = models.IntegerField(blank=True, null=True)
    amount = models.IntegerField(default=0)
    datetime = models.TextField(default="empty")
    order_id_data = models.TextField(default="empty")
    payment_id_data = models.TextField(default="empty")
    



class DeliveryBoy(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    vehicle_type = models.CharField(max_length=50)
    registration_number = models.CharField(max_length=20)
    delivery_zones = models.TextField()
    availability_timings = models.CharField(max_length=100)

    def __str__(self):
        return self.user.first_name  # or any other field you want to display


from django.utils import timezone

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    cart = models.IntegerField(blank=True, null=True)
    amount = models.IntegerField(default=0)
    datetime = models.TextField(default="empty")
    order_id_data = models.TextField(default="empty")
    payment_id_data = models.TextField(default="empty")
    status = models.CharField(max_length=100, default="pending")