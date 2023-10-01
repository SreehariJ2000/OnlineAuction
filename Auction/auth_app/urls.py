
from django.urls import path
from auth_app import views

urlpatterns = [
    
    path('signup/',views.Sign_up,name='signup'),
    path('handlelogin/',views.handlelogin,name='handlelogin'),
    path('handlelogout/',views.handlelogout,name='handlelogout'),
    path('activate/<uidb64>/<token>',views.ActivateAccountView.as_view(),name='activate'),
    path('request-reset-email/',views.RequestResetEmailView.as_view(),name="request-reset-email"),
    path("set-new-password/<uidb64>/<token>",views.SetNewPassword.as_view(),name="set-new-password")


]
