
from django.urls import path
from auth_app import views


urlpatterns = [
    
    path('signup/',views.Sign_up,name='signup'),
    
    path('handlelogin/',views.handlelogin,name='handlelogin'),
    path('handlelogout/',views.handlelogout,name='handlelogout'),
    path('activate/<uidb64>/<token>',views.ActivateAccountView.as_view(),name='activate'),
    path('request-reset-email/',views.RequestResetEmailView.as_view(),name="request-reset-email"),
    path("set-new-password/<uidb64>/<token>",views.SetNewPassword.as_view(),name="set-new-password"),
    path('update-profile/', views.update_profile, name='update-profile'),
    path('sellor_signup',views.sellor_signup,name='sellor_signup'),
    path('seller-dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('create-seller-profile/', views.create_seller_profile, name='create_seller_profile'),
    path('add_address/',views.add_address,name='add_address'),
     path('ongoing_bid/',views.ongoing_bid,name='ongoing_bid')


]
