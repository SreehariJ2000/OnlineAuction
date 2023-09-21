
from django.urls import path
from Auction_app import views

urlpatterns = [
    
    path('',views.index,name='index')
]
