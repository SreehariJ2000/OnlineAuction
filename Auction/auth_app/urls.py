
from django.urls import path
from auth_app import views

urlpatterns = [
    
    path('signup/',views.Sign_up,name='signup'),
    path('handlelogin/',views.handlelogin,name='handlelogin'),

]
