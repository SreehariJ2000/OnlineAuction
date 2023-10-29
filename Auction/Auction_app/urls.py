
from django.urls import path
from Auction_app import views

urlpatterns = [
    
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('customerhome/',views.CustomerHome,name='customerhome'),
    path('adminreg/',views.adminreg,name='adminreg'),
    path('add_product',views.add_product,name='add_product'),
    

]
