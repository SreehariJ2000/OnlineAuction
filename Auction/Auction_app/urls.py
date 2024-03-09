
from django.urls import path
from Auction_app import views
from .views import MostSoldProductsChartView
from .views import MostSoldProductsFilteredView

urlpatterns = [
    
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('customerhome/',views.CustomerHome,name='customerhome'),
    path('adminhome/',views.adminhome,name='admin'),
    path('deliveryboydashboard/',views.deliveryboydashboard,name='deliveryboydashboard'),
    path('add_product',views.add_product,name='add_product'),
    # path('api/get_categories/', views.get_categories, name='get_categories'),
    
    # path('api/get_subcategories/', views.get_subcategories, name='get_subcategories'),
   
    # admin side
    path('user_account/',views.user_account,name='user_account'),
    path('activate_user/<int:user_id>/', views.activate_user, name='activate_user'),
    path('deactivate_user/<int:user_id>/', views.deactivate_user, name='deactivate_user'),
    path('sellor_approval/',views.sellor_approval,name="sellor_approval"),
    path('approve_seller/<int:seller_id>/', views.approve_seller, name='approve_seller'),
    path('product_approval/',views.product_approval,name='product_approval'),
    path('more_product_details/<int:product_id>/',views.more_product_details,name='more_product_details'),
    path('approved_product/<int:product_id>/',views.approved_product,name='approved_product'),
    path('reject_product/<int:product_id>/', views.reject_product, name='reject_product'),
    path('second_winner/', views.second_winner, name='second_winner'),
     path('delivery_boys_list/', views.delivery_boys_list, name='delivery_boys_list'),
     path('activate_delivery_boy/<int:delivery_boy_id>/', views.activate_delivery_boy, name='activate_delivery_boy'),
    path('deactivate_delivery_boy/<int:delivery_boy_id>/', views.deactivate_delivery_boy, name='deactivate_delivery_boy'),
    path('register_delivery_boy/', views.register_delivery_boy, name='register_delivery_boy'),
      
    

#customer side
    path('live-auctions/', views.live_auctions, name='live_auctions'),
    path('upcoming-auctions/', views.upcoming_auctions, name='upcoming_auctions'),
    path('product/<int:product_id>/',views.bidding,name='bidding'),
    path('upcomming_detailed/<int:product_id>/',views.upcomming_detailed,name='upcomming_detailed'),
    path('place_bid/<int:product_id>/', views.place_bid, name='place_bid'),
    path('addtocart/',views.addtocart,name='addtocart'),
    path('winner_cart/', views.winner_cart, name='winner_cart'),
    path('auctionhistory/', views.auction_history, name='auction_history'),
    path('history_details/<int:product_id>',views.history_details,name='history_details'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('orderdetails',views.orderdetails,name='orderdetails'),
    path('download_invoice/<str:order_id>/', views.download_invoice, name='download_invoice'),
    path('vendor_info/<int:product_id>/', views.vendor_info, name='vendor_info'),
    path('submit_review/<int:seller_id>/', views.submit_review, name='submit_review'),
    path('chat/', views.chatwith, name='chat'),
    path('blog_post_list/', views.blog_post_list, name='blog_post_list'),
    path('blog/<int:blog_post_id>/', views.blog_post_detail, name='blog_post_detail'),
    
    
    #seller side
    path('product_status/', views.seller_products, name='seller_products'),
    path('progress_status/<int:product_id>',views.progress_status,name="progress_status"),
    path('contact-second-winner/<int:product_id>/<int:second_winner_id>/', views.contact_second_winner, name='contact_second_winner'),
    path('product_donotbuy_seconduser/<int:product_id>/',views.product_donotbuy_seconduser,name="product_donotbuy_seconduser"),
    path('rejected_products/', views.rejected_products, name='rejected_products'),
    path('start_reauction/', views.start_reauction_view, name='start_reauction'),
    path('most_sold_products_chart/', MostSoldProductsChartView.as_view(), name='most_sold_products_chart'),
    path('most_sold_products_filtered/', MostSoldProductsFilteredView.as_view(), name='most_sold_products_filtered'),
    path('add/', views.add_blog_post, name='add_blog_post'),




    #add delivery boy
    path('add_delivery_boys/',views.add_delivery_boys,name="deliveryboy"),
    path('Change_password/', views.Change_password, name='Change_password'),
]


