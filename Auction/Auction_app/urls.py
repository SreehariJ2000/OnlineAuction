
from django.urls import path
from Auction_app import views

urlpatterns = [
    
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('customerhome/',views.CustomerHome,name='customerhome'),
    path('adminhome/',views.adminhome,name='admin'),
    path('add_product',views.add_product,name='add_product'),
    path('api/get_categories/', views.get_categories, name='get_categories'),
    
    path('api/get_subcategories/', views.get_subcategories, name='get_subcategories'),
   
    # admin side
    path('user_account/',views.user_account,name='user_account'),
    path('activate_user/<int:user_id>/', views.activate_user, name='activate_user'),
    path('deactivate_user/<int:user_id>/', views.deactivate_user, name='deactivate_user'),
    path('sellor_approval/',views.sellor_approval,name="sellor_approval"),
    path('approve_seller/<int:seller_id>/', views.approve_seller, name='approve_seller'),

    
    

]
