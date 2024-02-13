from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Category),
admin.site.register(SubCategory),
admin.site.register(AddProduct),
admin.site.register(Bid),
admin.site.register(Cart),
admin.site.register(CartItems),
admin.site.register(RejectedProduct),
admin.site.register(DeliveryBoy),
admin.site.register(Order),
admin.site.register(UserPayment),