
from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from auth_app.models import *
from django.contrib.auth import get_user_model
User = get_user_model()

from django.db.models import Q



# Create your models here.

class ThreadManager(models.Manager):
    def by_user(self, **kwargs):
        user = kwargs.get('user')
        lookup = Q(first_person=user) | Q(second_person=user)
        qs = self.get_queryset().filter(lookup).distinct()
        return qs


class Thread(models.Model):
    first_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='thread_first_person')
    second_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='thread_second_person')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ThreadManager()
    class Meta:
        unique_together = ['first_person', 'second_person']


class ChatMessage(models.Model):
    thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.CASCADE, related_name='chatmessage_thread')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


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
    




from django.utils import timezone

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    cart = models.IntegerField(blank=True, null=True)
    amount = models.IntegerField(default=0)
    datetime = models.TextField(default="empty")
    order_id_data = models.TextField(default="empty")
    payment_id_data = models.TextField(default="empty")
    status = models.CharField(max_length=100, default="pending")




from textblob import TextBlob

class Review(models.Model):
    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    sentiment_rating = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Calculate sentiment rating using textblob
        blob = TextBlob(self.review_text)
        self.sentiment_rating = blob.sentiment.polarity
        super().save(*args, **kwargs)

  


class BlogPost(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    heading = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)


    def __str__(self):
        return self.heading
    



class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)


class TotalView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE)



class DeliveryBoy(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    vehicle_type = models.CharField(max_length=50)
    registration_number = models.CharField(max_length=20)
    delivery_zones = models.TextField()
    availability_timings = models.CharField(max_length=100)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    pincode = models.PositiveIntegerField()

    def __str__(self):
        return self.user.first_name  # or any other field you want to display




class DeliveryAssignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_boy = models.ForeignKey(DeliveryBoy, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(AddProduct, on_delete=models.CASCADE)  # Assuming Product model exists
    assigned_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, default='PENDING')

    def __str__(self):
        return f"DeliveryAssignment - {self.order} - {self.delivery_boy} - {self.status}"