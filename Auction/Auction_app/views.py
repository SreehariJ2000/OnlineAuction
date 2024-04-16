from django.shortcuts import render,redirect
from  auth_app.models import User
from django.db.models import Q
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import JsonResponse
from .models import *
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from django.contrib import messages
from decimal import Decimal
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from django.db.models import OuterRef, Subquery

import pandas as pd




# Create your views here.
@never_cache
def index(request):
    
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')


def CustomerHome(request):
    if 'username' in request.session:
        current_time = timezone.now()
        upcoming_auctions = AddProduct.objects.filter(
        auction_start_datetime__gt=current_time,admin_approval=True)

        response = render(request,'customer_home.html',{'upcoming_auctions': upcoming_auctions})
        response['Cache-Control'] = 'no-store,must-revalidate'
        return response
    else:
        return redirect('handlelogin')
    #return render(request,'customer_home.html')


@never_cache
@login_required(login_url="/auth_app/handlelogin/")

def adminhome(request):   
    return render(request, 'admin/adminhome.html')


def user_account(request):
    role_filter = request.GET.get('role')
    users = User.objects.filter(~Q(is_superuser=True))  # Exclude superusers by default

    if role_filter:
        users = users.filter(role=role_filter)

    context = {'User_profiles': users, 'role_filter': role_filter}
    return render(request, 'admin/usertable.html',context)


    
def activate_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = True
    user.save()
    subject = 'Account Activation'
    html_message = render_to_string('admin/activation_email.html', {'user': user})
    plain_message = strip_tags(html_message)
    from_email = 'hsree524@gmail.com'
    recipient_list = [user.email]
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
    return redirect('/user_account/')

def deactivate_user(request, user_id):
    user = User.objects.get(id=user_id)
    if user.is_superuser:
        return HttpResponse("You cannot deactivate the admin.")
    user.is_active = False
    user.save()
    subject = 'Account Deactivation'
    html_message = render_to_string('admin/deactivation_email.html', {'user': user})
    plain_message = strip_tags(html_message)
    from_email = 'hsree524@gmail.com'
    recipient_list = [user.email]
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
    # Send an email to the user here
    return redirect('/user_account/')



def sellor_approval(request):
    unapproved_sellers = SellerProfile.objects.filter(is_approved=False)
    messages.warning(request,"admin approved sucessfully")
    
    return render(request,'admin/pending_sellor_activation.html',{'unapproved_sellers': unapproved_sellers})



def approve_seller(request, seller_id):
    seller = SellerProfile.objects.get(pk=seller_id)
    seller.is_approved = True
    seller.save()
    subject = 'Your Seller Account Has Been Approved'
    message = 'Dear {},\n\nYour seller account has been approved by the admin. You can now log in and start using your account.\n\nLogin Link: http://127.0.0.1:8000/auth_app/handlelogin/'.format(seller.user.first_name)
    from_email = 'hsree524@gmail.com'  # Replace with your email address
    recipient_list = [seller.user.email]
    
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    
    return redirect('/sellor_approval/')



@login_required(login_url="/auth_app/handlelogin/")
def approved_product(request,product_id):
    product = AddProduct.objects.get(pk=product_id)
    product.admin_approval = True
    product.save()
    subject = 'Your Product Approval'
    message = f'Your product "{product.product_name}" has been approved.'
    from_email = 'hsree524@gmail.com'  
    recipient_list = [product.seller.user.email]  

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

    return redirect('/product_approval/') 







def reject_product(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(AddProduct, id=product_id)
        product.delete()
        return redirect('/product_approval/')  

    #return render(request, 'your_template_name.html')  




def seller_products(request):
    # Retrieve products for the current seller
    seller_products = AddProduct.objects.filter(seller=request.user.sellerprofile)
    curent_time=timezone.now()

    context = {
        'seller_products': seller_products,
        'time': curent_time
    }

    return render(request, 'sellor/seller_product_status.html', context)



@login_required(login_url="/auth_app/handlelogin/")
def add_product(request):
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all() 
    if request.method == 'POST':
        # Retrieve data from the form
        category = request.POST.get('category')
        sub_category = request.POST.get('sub_category')
        print(category,sub_category,"11111111111111111111111111111111111")
        product_name = request.POST.get('product_name')
        current_price=request.POST.get('current_price')
        tags = request.POST.get('tags')
        about_product = request.POST.get('about_product')
        auction_start_datetime = request.POST.get('auction_start_datetime')
        auction_end_datetime = request.POST.get('auction_end_datetime')
        image1 = request.FILES['image1']
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')
        image4 = request.FILES.get('image4')
        authentication_certificate = request.FILES['authentication_certificate']
          

        
        add_product = AddProduct(
            category=category,
            sub_category=sub_category,
            product_name=product_name,
            tags=tags,
            about_product=about_product,
            current_price=current_price,
            auction_start_datetime=auction_start_datetime,
            auction_end_datetime=auction_end_datetime,
            image1=image1,
            image2=image2,
            image3=image3,
            image4=image4,
            authentication_certificate=authentication_certificate,
            seller=request.user.sellerprofile  
        )
        add_product.save()
        messages.success(request,"waiting for approval")
        return redirect('/add_product')  
    return render(request,'sellor/add_product.html',{'categories': categories, 'subcategories': subcategories})





@login_required(login_url="/auth_app/handlelogin/")
def product_approval(request):
    unapproved_products = AddProduct.objects.filter(admin_approval=False)
    
    return render(request,'admin/pending_product.html',{'unapproved_products': unapproved_products})



def auction_history(request):
    latest_bids_subquery = Bid.objects.filter(bidder=request.user, product=OuterRef('product')).order_by('-timestamp').values('id')[:1]
    user_bids = Bid.objects.filter(id__in=Subquery(latest_bids_subquery))
    products_participated = AddProduct.objects.filter(bid__in=user_bids, auction_end_datetime__lt=timezone.now())
    context = {
        'products_participated': products_participated,
    }

    return render(request, 'customer/auctionhistory.html', context)



#sellor
def progress_status(request,product_id):
    user = request.user
    product = AddProduct.objects.get(id=product_id)
    
    bids = Bid.objects.filter(product_id=product_id).order_by('-bid_amount') 

    bidder_names = []
    for bid in bids:
        try:
            profile = Profile.objects.get(user=bid.bidder)
            bidder_names.append(profile.bidder_id)
        except Profile.DoesNotExist:
            bidder_names.append("N/A")

    context = {
        'product': product,
        'user_data': user,
        'bids': zip(bids, bidder_names),  
    }
    return render (request,'sellor/progressstatus.html',context)



def history_details(request,product_id):
    user = request.user
    product = AddProduct.objects.get(id=product_id)
    
    bids = Bid.objects.filter(product_id=product_id).order_by('-bid_amount') 

    bidder_names = []
    for bid in bids:
        try:
            profile = Profile.objects.get(user=bid.bidder)
            bidder_names.append(profile.bidder_id)
        except Profile.DoesNotExist:
            bidder_names.append("N/A")

    context = {
        'product': product,
        'user_data': user,
        'bids': zip(bids, bidder_names),  # Pair each bid with its bidder name
    }
    return render(request, 'customer/history_detail.html',context)






@login_required(login_url="/auth_app/handlelogin/")
def more_product_details(request,product_id):
    product = AddProduct.objects.get(id=product_id)
    return render(request,'admin/more_product_detail.html', {'product': product})



def live_auctions(request):
    
    current_time = timezone.now()
    live_auctions = AddProduct.objects.filter(
        auction_start_datetime__lte=current_time,
        auction_end_datetime__gt=current_time,admin_approval=True
        
    )
    # if live_auctions.exists():
    #     for auction in live_auctions:
    #         print("Auction Start Date:", auction.auction_start_datetime)
    # else:
    #          print("No live auctions.")

    # all_products = AddProduct.objects.all()
    # for product in all_products:
    #       print("Product Name:", product.product_name)
    #       print("Auction Start Date:", product.auction_start_datetime)

    return render(request, 'live_auction.html', {'live_auctions': live_auctions})


@never_cache
@login_required(login_url="/auth_app/handlelogin/")
def upcoming_auctions(request):
    
    current_time = timezone.now()
    upcoming_auctions = AddProduct.objects.filter(
    auction_start_datetime__gt=current_time,admin_approval=True
  )

    return render(request, 'upcoming_auctions.html', {'upcoming_auctions': upcoming_auctions})





def bidding(request, product_id):
    user = request.user
    product = AddProduct.objects.get(id=product_id)
    current_time = timezone.now()
    if current_time > product.auction_end_datetime:
        return redirect('/live-auctions/')

    # bids = Bid.objects.filter(product_id=product_id)
    
    bids = Bid.objects.filter(product_id=product_id).order_by('-bid_amount') 

    bidder_names = []
    for bid in bids:
        try:
            profile = Profile.objects.get(user=bid.bidder)
            bidder_names.append(profile.bidder_id)
        except Profile.DoesNotExist:
            bidder_names.append("N/A")

    context = {
        'product': product,
        'user_data': user,
        'bids': zip(bids, bidder_names),  # Pair each bid with its bidder name
    }
    return render(request, 'customer/bidding.html', context)



@login_required(login_url="/auth_app/handlelogin/")
def upcomming_detailed(request,product_id):
    user=request.user
    product=AddProduct.objects.get(id=product_id)
    context={
        'user_data':user,
        'product':product
    }
    return render(request,'customer/upcomming_detailed.html',context)







def place_bid(request,product_id):
    if request.method == 'POST':
        bid_amount = Decimal(request.POST.get('bid_amount'))
        product = AddProduct.objects.get(pk=product_id)

        try:
            profile = Profile.objects.get(user=request.user)
            if not profile.bidder_id:
                messages.error(request, "You need to set a bidder_id in your profile before placing a bid.")
                return redirect('/update-profile')
        except Profile.DoesNotExist:
            messages.error(request, "You need to create a profile with a bidder_id before placing a bid.")
            return redirect('update-profile')

        if product.current_highest_bid < 1:
            if bid_amount < product.current_price:
                messages.error(request,"Your Bid should be greater than the Current Price.")
                return redirect('bidding', product_id=product_id)
            

        if bid_amount > product.current_highest_bid:
            product.current_highest_bid = bid_amount
            product.save()

            Bid.objects.create(product=product, bidder=request.user, bid_amount=bid_amount)
        
            return redirect('bidding', product_id=product_id)
        else:
            messages.success(request," use higher amount than now ")
            return redirect('bidding', product_id=product_id)
            




import threading

def send_winner_email(product, highest_bid):
    subject = 'Congratulations! You are the Winner!'
    context = {
        'product': product,
        'highest_bid': highest_bid,
        'purchase_link': 'your_purchase_link',  # Replace with the actual purchase link
    }
    html_message = render_to_string('winner_email_template.html', context)
    plain_message = strip_tags(html_message)
    from_email = 'hsree524@gmail.com'  # Replace with your email
    to_email = [highest_bid.bidder.email]  # Use the winner's email
    send_mail(subject, plain_message, from_email, to_email, html_message=html_message)

def addtocart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        request.session['product_id'] = product_id
        product = get_object_or_404(AddProduct, id=product_id)

        highest_bid = Bid.objects.filter(product=product).order_by('-bid_amount').first()

        if highest_bid:
            user_cart, created = Cart.objects.get_or_create(user=highest_bid.bidder, is_paid=False)    
            cart_item, created = CartItems.objects.get_or_create(cart=user_cart, product=product)

            # Send email to the winner using threading
            email_thread = threading.Thread(target=send_winner_email, args=(product, highest_bid))
            email_thread.start()

            return JsonResponse({'success': True, 'message': 'Product added to cart successfully.'})
        else:
            return JsonResponse({'success': False, 'message': 'No bids found for the specified product.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})




# from django.db.models import Sum

# def winner_cart(request):
#     winner_cart = Cart.objects.filter(user=request.user, is_paid=False).first()
#     total_amount = CartItems.objects.filter(cart=winner_cart).aggregate(Sum('product__current_highest_bid'))['product__current_highest_bid__sum']
    
#     if winner_cart:
#         cart_items = CartItems.objects.filter(cart=winner_cart)
#         context = {'cart_items': cart_items, 'total_amount': total_amount}
#         return render(request, 'customer/winner_cart.html', context)
#     else:
#         return render(request, 'customer/winner_cart.html')




from django.http import JsonResponse

def start_reauction_view(request):
    if request.method == 'POST':
        
        start_date = request.POST.get('start_date')        
        end_date = request.POST.get('end_date')
        pid=request.POST.get('product_id')
        

        if start_date:
            print("start date",start_date)
        if pid: 
            print("Product ID:", pid)

            
        # Fetch the AddProduct with the given pid
        product = get_object_or_404(AddProduct, pk=pid)

        # Update the start time and end time
        product.auction_start_datetime = start_date
        product.auction_end_datetime = end_date
        product.save()

        # Set reauction to True in RejectedProduct
        rejected_product = RejectedProduct.objects.get(product=product)
        rejected_product.reauction = True
        rejected_product.save()
            
        
        
        return JsonResponse({'status': 'success', 'message': 'Reauction started successfully'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})



from django.views.generic import TemplateView
from django.db.models import Sum
from django.db.models.functions import TruncMonth

class MostSoldProductsChartView(TemplateView):
    template_name = 'chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['labels'] = self.get_labels()
        context['data'] = self.get_data()
        return context

    def get_labels(self):
        return [str(item['month']) for item in self.get_monthly_data()]

    def get_data(self):
        return [item['total_sales'] for item in self.get_monthly_data()]

    def get_monthly_data(self):
        return ProductSale.objects.annotate(month=TruncMonth('sale_date')).values('month').annotate(total_sales=Sum('sale_amount')).order_by('month')



from django.views.generic.list import ListView
from django.db.models import Sum

from django.db.models import Sum

class MostSoldProductsFilteredView(ListView):
    model = AddProduct
    template_name = 'most_sold_products_filtered.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = AddProduct.objects.annotate(total_sales=Sum('productsale__sale_amount')).order_by('-total_sales')
        
        month_filter = self.request.GET.get('month')
        if month_filter:
            # Convert the month string to a valid numeric value
            try:
                month_numeric = int(month_filter.split('-')[1])
            except ValueError:
                # Handle the case where the month string is not a valid number
                month_numeric = None
            
            if month_numeric is not None:
                # Use the Bid model's relationship with AddProduct to filter by timestamp
                queryset = queryset.filter(bid__timestamp__month=month_numeric)
        
        return queryset



from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from django.db.models import F

def winner_cart(request):
    winner_cart = Cart.objects.filter(user=request.user, is_paid=False).first()

    if winner_cart:
        expired_products = CartItems.objects.filter(
            cart=winner_cart,
            #product__auction_end_datetime__lt=timezone.now() - timedelta(hours=24)
            product__auction_end_datetime__lt=timezone.now() - timedelta(hours=24)
        )

        for item in expired_products:
            product_name = item.product.product_name
            user_email = request.user.email
            send_mail(
                f'Product Removed from Cart - {product_name}',
                f"Dear {request.user.username},\n\n"
                f"We regret to inform you that the product '{product_name}' has been removed from your cart "
                f"as the auction end date + 3 minutes has passed. The product will be offered to the second winner.\n\n"
                f"Please note that, due to not purchasing the product, your account may be deactivated.\n\n"
                f"Thank you for your participation.",
               'hsree524@gmail.com',   
               [user_email],
               fail_silently=False,
)

        expired_products.delete()
        total_amount = CartItems.objects.filter(cart=winner_cart).aggregate(Sum('product__current_highest_bid'))['product__current_highest_bid__sum']
        cart_items = CartItems.objects.filter(cart=winner_cart)

        context = {'cart_items': cart_items, 'total_amount': total_amount}
        return render(request, 'customer/winner_cart.html', context)
    else:
        return render(request, 'customer/winner_cart.html')




from django.shortcuts import render
from django.utils import timezone
from django.db.models import F
from .models import Cart, CartItems, AddProduct, Bid, User

def second_winner(request):
    # Get products with auction end date + 2 minutes and is_live is false
    products_to_process = AddProduct.objects.filter(
        is_live=False,
        auction_end_datetime__lte=timezone.now() + timezone.timedelta(minutes=2),
    ).exclude().distinct()

    # Initialize lists to store winner and second winner details
    winners = []
    second_winners = []

    # Loop through each product to find winners
    for product in products_to_process:
        # Get the highest bid for the product
        highest_bid = Bid.objects.filter(product=product).order_by('-bid_amount').first()

        if highest_bid:
            winner = highest_bid.bidder
            winners.append({ 'product_id':product.pk ,'product_name': product.product_name, 'winner_name': winner.username})

            # Get the second highest bid for the product, excluding the first winner
            second_highest_bid = Bid.objects.filter(product=product, bid_amount__lt=highest_bid.bid_amount).exclude(bidder=winner).order_by('-bid_amount').first()
            if second_highest_bid:
                second_winner = second_highest_bid.bidder
                second_winners.append({'winner_id':second_winner.pk, 'product_name': product.product_name, 'second_winner_name': second_winner.username})

    context = {'winners': winners, 'second_winners': second_winners}
    return render(request, 'admin/second_winner.html', context)










from django.shortcuts import render
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Bid, AddProduct, User
import threading

@login_required
def contact_second_winner(request, product_id, second_winner_id):
    try:
        product = AddProduct.objects.get(pk=product_id)
        second_winner = User.objects.get(pk=second_winner_id)
    except (AddProduct.DoesNotExist, User.DoesNotExist):
        return HttpResponse("Invalid product or second winner ID")

    # Compose the email content
    subject = f"Congratulations! You are the Second Winner for {product.product_name}"
    
    # Render the HTML template with dynamic data
    html_message = render_to_string('email_template.html', {
        'second_winner': second_winner,
        'product': product,
       
    })

    # Send the email using a separate thread
    email_thread = threading.Thread(target=send_email_in_thread, args=(subject, html_message, 'hsree524@gmail.com', [second_winner.email]))
    email_thread.start()

    return HttpResponse("contact second winner Success")

def send_email_in_thread(subject, message, from_email, recipient_list):
    # Send the HTML email
    send_mail(subject, strip_tags(message), from_email, recipient_list, html_message=message)





def product_donotbuy_seconduser(request,product_id):
    product = AddProduct.objects.get(pk=product_id)

    RejectedProduct.objects.create(product=product)
    return HttpResponse("Thankyou for your response!!!!")
    


def rejected_products(request):
    rejected_products = RejectedProduct.objects.filter(reauction=False)
    return render(request, 'sellor/rejected_product.html', {'rejected_products': rejected_products})



from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
 
 
# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
 

def checkout(request):
    # Fetch the user's cart item 
    user_cart = Cart.objects.get(user=request.user,is_paid=False)
    cart_items = CartItems.objects.filter(cart=user_cart)
    total_amount = sum(item.product.current_highest_bid for item in cart_items)

    user = request.user
    try:
        address = Address.objects.get(user=user)
    except Address.DoesNotExist:
        return redirect('/add_address')
    
    currency = 'INR'
    amount = int(total_amount * 100)  
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))

    razorpay_order_id = razorpay_order['id']
    callback_url = '/paymenthandler/'
 
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    context['total_amount'] = total_amount
    context['address'] = address
    
    return render(request, 'customer/checkout.html', context=context)


from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from django.db import models

from geopy.geocoders import Nominatim


@require_POST

   


@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
       
        try:
            print("111111111111")
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
           
            print(razorpay_order_id)
            
            print("2222222")
            print(payment_id,razorpay_order_id,signature)
            
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }


            user_cart = Cart.objects.get(user=request.user,is_paid=False)
            cart_items = CartItems.objects.filter(cart=user_cart)
            total_amount = sum(item.product.current_highest_bid for item in cart_items)
            print("Total Amount ffffffffffffff",total_amount)

 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            
            print("55555555555555555555555")
            print(result)

           
            if result is not None:
                current_datetime = timezone.now()
                user_payment_instance = UserPayment.objects.create(
                    user=request.user,
                    amount=total_amount,
                    datetime=current_datetime,
                    order_id_data=razorpay_order_id,
                    payment_id_data=payment_id,)
                cart = get_object_or_404(Cart, user=request.user, is_paid=False)


                order_instance = Order.objects.create(
                    user=request.user,
                    cart=user_cart.id,
                    amount=total_amount,
                    datetime=current_datetime,
                    order_id_data=razorpay_order_id,
                    payment_id_data=payment_id,
                    status="completed"  # Set the status to completed or any other desired value
                )

                product_id = request.session.get('product_id')
                product = get_object_or_404(AddProduct, id=product_id)
                print("ooo")
                
                
               
                user_address = Address.objects.get(user=request.user) 
                user=request.user
                print("ppp")
                print("User Address:", user_address)
                delivery_boys = DeliveryBoy.objects.filter(pincode=user_address.pincode)
                print("qqq")
                print("Delivery Boys:", delivery_boys)
                selected_delivery_boy = delivery_boys.first()  
                print("rrr")
                print("Selected Delivery Boy:", selected_delivery_boy)
                
                delivery_assignment = DeliveryAssignment.objects.create(
                   user=user,
                   delivery_boy=selected_delivery_boy,
                   order=order_instance,
                    product=product
                    )



                try:
                    cart.is_paid = True
                    cart.save()                  
                    

                    cart_items = CartItems.objects.filter(cart=cart)
                    for cart_item in cart_items:
                        product = cart_item.product
                        product.is_live = True
                        product.save()
                      
                    return redirect('orderdetails')
                except:
                 
                    return HttpResponse("some thing went wrong !! please try again")
            else:
 
                
                return  HttpResponse("some thing went wrong !! please try again")
        except:
 
            return HttpResponse("Payment failed . please try again")
    else:
      
        return  HttpResponse("some thing went wrong !! please try again")
    



# def orderdetails(request):
   
#     orders = Order.objects.filter(user=request.user)
#     order_details = []
#     for order in orders:
#         user_cart = get_object_or_404(Cart, id=order.cart)
#         cart_items = CartItems.objects.filter(cart=user_cart)
#         product_details = []

#         for cart_item in cart_items:
#             product = cart_item.product
#             product_details.append({
#                 'product_name': product.product_name,
#                 'image_url': product.image1.url,  # Change this to the appropriate field for the image
#                 'amount': order.amount,
#                 'order_id': order.order_id_data,
#                 'status': order.status,
#             })

#         order_details.append(product_details)

#     context = {'order_details': order_details}
#     return render(request, 'customer/orderdetails.html', context)
    



def orderdetails(request):
    # Retrieve orders for the logged-in user
    orders = Order.objects.filter(user=request.user)
    order_details = []

    for order in orders:
        user_cart = get_object_or_404(Cart, id=order.cart)
        cart_items = CartItems.objects.filter(cart=user_cart)

        # Create a list to store details of each product in the order
        product_details = []

        for cart_item in cart_items:
            product = cart_item.product
            product_details.append({
                'product_id':product.pk,
                'sellor_id':product.seller.pk,
                'product_name': product.product_name,
                'image_url': product.image1.url,  
                'amount': order.amount,
                'order_id': order.order_id_data,
                'status': order.status,
            })

        # Fetch addresses for the user
        addresses = Address.objects.filter(user=request.user)

        order_details.append({
            'product_details': product_details,
            'addresses': addresses,
        })

    context = {'order_details': order_details}
    return render(request, 'customer/orderdetails.html', context)



from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.shortcuts import get_object_or_404

def download_invoice(request, order_id):
    # Query the Order model using the order_id field
    order = get_object_or_404(Order, order_id_data=order_id)
    cart_items = CartItems.objects.filter(cart=order.cart)
    product_names = [item.product.product_name for item in cart_items]

    addresses = Address.objects.filter(user=request.user)
    order_details=[]

    order_details.append({
            
            'addresses': addresses,
        })

    template_path = 'customer/invoice_template.html'
    context = {'order': order,'product_names': product_names,'order_details': order_details}
    template = get_template(template_path)
    html = template.render(context)

    # Create a response object with appropriate headers for downloading
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=invoice_{order.order_id_data}.pdf'

    # Create a PDF file
    pisa_status = pisa.CreatePDF(html, dest=response)

    # Check if the PDF creation was successful
    if pisa_status.err:
        return HttpResponse('Error creating PDF', content_type='text/plain')

    return response

from django.core.mail import EmailMessage


def sendmail_in_thread(subject, html_message, to_email):
    email = EmailMessage(subject, html_message, to=to_email)
    email.content_subtype = "html"
    email.send()

def add_delivery_boys(request):
    if request.method == 'POST' and request.FILES['xl_sheet']:
        xl_sheet = request.FILES['xl_sheet']
        delivery_added_successfully = False

        try:
            df = pd.read_excel(xl_sheet)
            

            for _, row in df.iterrows():
                # Create a unique username and password for each delivery boy
                username = row['Email']
                password = User.objects.make_random_password()

                user = User.objects.create_user(
                    username=username,
                    email=row['Email'],
                    password=password,
                    first_name=row['Firstname'],
                    last_name=row['Lastname'],
                    role='SERVICE'
                )

                contact_number = row['Contact Number']
                address = row['Address']
                vehicle_type = row['Vehicle Type']
                registration_number = row['Registration Number']
                delivery_zones = row['Delivery Zones']
                availability_timings = row['Availability Timings']
                city=row['City']
                state=row['State']
                pincode=row['Pincode']

                delivery_boy = DeliveryBoy.objects.create(
                    user=user,
                    contact_number=contact_number,
                    address=address,
                    vehicle_type=vehicle_type,
                    registration_number=registration_number,
                    delivery_zones=delivery_zones,
                    availability_timings=availability_timings,
                    city=city,
                    state=state,
                    pincode=pincode
                )

                # Send an email to the delivery boy with their password
                subject = 'Welcome to the Delivery Service'
                html_message = render_to_string('email_to_deliveryboy.html', {
                    'firstname': row['Firstname'],
                    'password': password,
                })
                to_email = [row['Email']]

                

                # Use a thread to send the email asynchronously
                email_thread = threading.Thread(target=sendmail_in_thread, args=(subject, html_message, to_email))
                email_thread.start()
            delivery_added_successfully = True 
               
                
           

        except Exception as e:
            messages.error(request, f'Error processing the Excel sheet: {e}')

        if delivery_added_successfully:
            messages.success(request, 'Delivery boys added successfully.')

    
    return render(request, 'admin/add_delivery_boys.html',{})

@never_cache
@login_required(login_url="/auth_app/handlelogin/")
def deliveryboydashboard(request):
    return render(request,'Delivery/deliverydashboard.html')



from django.contrib.auth import update_session_auth_hash

@login_required
def Change_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password == confirm_password:
            user = request.user
            user.set_password(new_password)
            user.save()

            # Update session to prevent the user from being logged out
            update_session_auth_hash(request, user)

            messages.success(request, 'Password changed successfully.')
            return redirect('handlelogin')
        else:
            messages.error(request, 'Passwords do not match.')

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})



def delivery_boys_list(request):
    delivery_boys = DeliveryBoy.objects.all()
    return render(request, 'admin/delivery_boys_list.html', {'delivery_boys': delivery_boys})


# views.py
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def activate_delivery_boy(request, delivery_boy_id):
    delivery_boy = get_object_or_404(DeliveryBoy, id=delivery_boy_id)
    delivery_boy.user.is_active = True
    delivery_boy.user.save()

    # Send activation email
    send_mail(
        'Your account has been activated',
        'Dear {},\n\nYour account has been activated.'.format(delivery_boy.user.get_full_name()),
        'your_email@example.com',  # Set your email here
        [delivery_boy.user.email],
        fail_silently=False,
    )

    messages.success(request, f"{delivery_boy.user.get_full_name} has been activated.")
    return redirect('delivery_boys_list')

def deactivate_delivery_boy(request, delivery_boy_id):
    delivery_boy = get_object_or_404(DeliveryBoy, id=delivery_boy_id)
    delivery_boy.user.is_active = False
    delivery_boy.user.save()

    # Send deactivation email
    send_mail(
        'Your account has been deactivated',
        'Dear {},\n\nYour account has been deactivated.'.format(delivery_boy.user.get_full_name()),
        'your_email@example.com',  # Set your email here
        [delivery_boy.user.email],
        fail_silently=False,
    )

    messages.success(request, f"{delivery_boy.user.get_full_name} has been deactivated.")
    return redirect('delivery_boys_list')




# added by admin
from django.contrib.auth import get_user_model
from django.db import IntegrityError


def sendmail_in_thread(subject, html_message, to_email):
    email = EmailMessage(subject, strip_tags(html_message), to=to_email)
    email.content_subtype = "html"
    email.send()



def register_delivery_boy(request):
    if request.method == 'POST':
        try:
            # Get form data
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            contact_number = request.POST.get('contact_no')
            address = request.POST.get('address')
            vehicle_type = request.POST.get('vehicle_type')
            registration_number = request.POST.get('registration')
            

            # Generate a random password
            random_password = get_user_model().objects.make_random_password()

            # Attempt to create a new user
            user = get_user_model().objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=email,
                email=email,
                password=random_password,
                role='SERVICE'
            )

            # Create the delivery boy with the provided contact number
            delivery_boy = DeliveryBoy.objects.create(
                user=user,
                contact_number=contact_number,
                address=address,
                vehicle_type=vehicle_type,
                registration_number=registration_number,
                delivery_zones="kerala",
                availability_timings="8.00 to 10",
                city="pta",
                state="kerala",
                pincode=689693
            )

            # Send email with the random password
            subject = 'Welcome to the Delivery Service'
            html_message = render_to_string('email_to_deliveryboy.html', {'firstname': user.first_name, 'password': random_password})
            to_email = [email]

            # Use a thread to send the email asynchronously
            email_thread = threading.Thread(target=sendmail_in_thread, args=(subject, html_message, to_email))
            email_thread.start()

            # Check if success message has already been displayed
            if 'success_message_displayed' not in request.session:
                # Set a success message
                messages.success(request, 'Delivery boys added successfully.')
                # Set a flag in session to indicate that the message has been displayed
                request.session['success_message_displayed'] = True

            # Redirect to the same URL to clear POST data
            return redirect('register_delivery_boy')  # Change 'register_delivery_boy' to the appropriate URL name

        except IntegrityError:
            messages.error(request, 'An error occurred while adding the delivery boy.')

    # Render the registration page template
    return render(request, 'admin/add_delivery_boys.html')


from django.db.models import Count

def vendor_info(request, product_id):
    print("ffffffffffffffffffffff")
    product = get_object_or_404(AddProduct, pk=product_id)
    seller_id = product.seller_id
    seller_products = AddProduct.objects.filter(seller_id=seller_id)
    seller_reviews=Review.objects.filter(seller_id=seller_id)
    unique_reviewers = seller_reviews.values('reviewer_id').annotate(count=Count('reviewer_id'))
    return render(request, 'customer/vendor_info.html', {'seller_products': seller_products,'seller_reviews':seller_reviews,'unique_reviewers': unique_reviewers})



def review_status(request):
    reviews = Review.objects.all()
    sentiment = request.GET.get('sentiment')
    if sentiment == 'positive':
        reviews = reviews.filter(sentiment_rating__gte=0)
    elif sentiment == 'negative':
        reviews = reviews.filter(sentiment_rating__lt=0)
    elif sentiment =='full':
         reviews = Review.objects.all()
    return render(request, 'admin/review_status.html', {'reviews': reviews})




@login_required
def submit_review(request, seller_id):
    print(seller_id,'****************888')
    
    if request.method == 'POST':
        user=request.user
        seller_profile = get_object_or_404(SellerProfile, pk=seller_id)
        if not Review.objects.filter(reviewer=user, seller=seller_profile).exists():

             review_text = request.POST.get('review_text')
             reviewer = request.user
             Review.objects.create(seller=seller_profile, reviewer=reviewer, review_text=review_text)
             return redirect('orderdetails')
        else:
            messages.success(request,"This is Already reviewed")
    return redirect('orderdetails')


from Auction_app.models import Thread
def chatwith(request):
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
    context = {
        'Threads': threads
    }
    return render(request,'messages.html',context)




from .forms import BlogPostForm
def add_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.seller = request.user
            blog_post.save()
            return redirect('/add')  # Redirect to the blog post list page
    else:
        form = BlogPostForm()

    return render(request, 'sellor/add_blog_post.html', {'form': form})


@never_cache
@login_required(login_url="/auth_app/handlelogin/")
def blog_post_list(request):
    blog_posts = BlogPost.objects.all()
    top_three_posts = BlogPost.objects.order_by('-views')[:3]
    return render(request, 'customer/blog_post_list.html', {'blog_posts': blog_posts,'top_three_posts':top_three_posts})



@never_cache
@login_required(login_url="/auth_app/handlelogin/")
def blog_post_detail(request, blog_post_id):
    blog_post = get_object_or_404(BlogPost, id=blog_post_id)
    user = request.user

    if not TotalView.objects.filter(user=user, blog=blog_post).exists():
        TotalView.objects.create(user=user, blog=blog_post)

        blog_post.views += 1
        blog_post.save()

    varr=True
    if request.method == 'POST':
        if 'like_button' in request.POST:
            user = request.user
            if user.is_authenticated:
                # Check if the user has already liked the post
                if not Like.objects.filter(user=user, blog_post=blog_post).exists():
                    varr=False
                    # If not, add a new like
                    Like.objects.create(user=user, blog_post=blog_post)
                    blog_post.likes_count = blog_post.like_set.count()
                    blog_post.save()
                else:
                    messages.success(request,"you already like this post")
            else:
                return HttpResponse("Please log in to like the post.")
    
    return render(request, 'customer/blog_post_detail.html', {'blog_post': blog_post,'var':varr})






def ship_order(request):
    pending_assignments = DeliveryAssignment.objects.filter(status='PENDING')

    # Fetch corresponding address details
    addresses = {}
    for assignment in pending_assignments:
        # Retrieve the address associated with the user in the delivery assignment
        address = Address.objects.filter(user=assignment.user).first()
        if address:
            addresses[assignment.id] = address

    context = {
        'pending_assignments': pending_assignments,
        'addresses': addresses,
    }
    return render(request, 'sellor/ship_order.html', context)




def mark_as_shipped(request, assignment_id):
    if request.method == 'POST':
        assignment = DeliveryAssignment.objects.get(id=assignment_id)
        assignment.status = 'SHIPPED'
        assignment.save()
    return redirect('ship_order')


def trackmyorder(request):
    user=request.user
    order=DeliveryAssignment.objects.filter(user=user)
    context={
        'order':order
    }
    return render (request,'customer/trackmyorder.html',context)


def new_orders(request):
    delivery_boy = request.user.deliveryboy
    orders = DeliveryAssignment.objects.filter(delivery_boy=delivery_boy,status='SHIPPED')
    addresses = {}
    for assignment in orders:
        # Retrieve the address associated with the user in the delivery assignment
        address = Address.objects.filter(user=assignment.user).first()
        if address:
            addresses[assignment.id] = address

    context = {
              'pending_assignments': orders,
              'addresses': addresses, }
    
    return render(request,'Delivery/new_orders.html',context)

# views.py
import random

def out_for_delivery(request):
    delivery_boy = request.user.deliveryboy
    orders = DeliveryAssignment.objects.filter(delivery_boy=delivery_boy,status='OUT')
    addresses = {}
    for assignment in orders:
        # Retrieve the address associated with the user in the delivery assignment
        address = Address.objects.filter(user=assignment.user).first()
        if address:
            addresses[assignment.id] = address

    context = {
              'pending_assignments': orders,
              'addresses': addresses }
    if request.method == 'POST':
        # Generate 6-digit OTP
        otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])

        # Send email to customer
        delivery_assignment_id = request.POST.get('delivery_assignment_id')
        delivery_assignment = DeliveryAssignment.objects.get(pk=delivery_assignment_id)
        customer_email = delivery_assignment.user.email
        product_name = delivery_assignment.product.product_name

        message = f'Your {product_name} is out for delivery.'
        Notification.objects.create(user=delivery_assignment.user, message=message)
        send_mail(
            'Your Order is Out for Delivery',
            f'Your {product_name} is out for delivery. Your OTP is: {otp}',
            'from@example.com',  # Sender's email
            [customer_email],  # List of recipient emails
            fail_silently=False,
        )

        # Store OTP in the database
        otp_instance = OTP.objects.create(delivery_assignment=delivery_assignment, otp=otp)
        delivery_assignment.status='OUT'
        delivery_assignment.save() 

        return render(request, 'Delivery/out_for_delivery.html', {'otp_sent': True})
    else:
        return render(request, 'Delivery/out_for_delivery.html',context)



from django.http import JsonResponse

def check_notifications(request):
   
    notifications = Notification.objects.filter(user=request.user, read=False)
    notification_count = notifications.count()
    # Mark notifications as read
    notifications.update(read=True)
    # Prepare JSON response
    response_data = {
        'notification_count': notification_count,
        'notifications': [notif.message for notif in notifications]
    }
    return JsonResponse(response_data)



def verify_otp(request):
    if request.method == 'POST':
        delivery_assignment_id = request.POST.get('delivery_assignment_id')
        entered_otp = request.POST.get('otp')
        try:
            otp_instance = OTP.objects.get(delivery_assignment_id=delivery_assignment_id)
        except OTP.DoesNotExist:
            return HttpResponse('OTP not found.', status=400)

        if entered_otp == otp_instance.otp:
            delivery_assignment = DeliveryAssignment.objects.get(id=delivery_assignment_id)
            delivery_assignment.status='DELIVERED'
            delivery_assignment.save()
            

           
            # otp_instance.delete()  
            return HttpResponse('Delivery successful!')
        else:
            # OTP doesn't match
            return HttpResponse('Invalid OTP.', status=400)




import folium
from django.shortcuts import render

# def show_route(request):
#     # Random latitude and longitude coordinates for Pathanamthitta, Kerala, India
#     latitude_delivery_boy = 9.2667
#     longitude_delivery_boy = 76.7833

#     latitude_customer = 9.2647
#     longitude_customer = 76.7875

#     # Create a Folium map centered on the delivery boy's location
#     delivery_boy_location = (latitude_delivery_boy, longitude_delivery_boy)
#     map = folium.Map(location=delivery_boy_location, zoom_start=12)

#     # Add markers for delivery boy and customer locations
#     folium.Marker(location=delivery_boy_location, popup='Delivery Boy').add_to(map)
#     folium.Marker(location=(latitude_customer, longitude_customer), popup='Customer').add_to(map)

#     # Add route between delivery boy and customer
#     folium.PolyLine(locations=[delivery_boy_location, (latitude_customer, longitude_customer)], color='blue').add_to(map)

#     # Render the map in the template
#     return render(request, 'map.html', {'map': map._repr_html_()})

import folium
from folium import plugins
from django.shortcuts import render

def show_route(request):
    return render(request, 'map.html')
