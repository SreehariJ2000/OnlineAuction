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


       
@login_required(login_url="/auth_app/handlelogin/")
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


@login_required(login_url="/auth_app/handlelogin/")
def upcoming_auctions(request):
    
    current_time = timezone.now()
    upcoming_auctions = AddProduct.objects.filter(
    auction_start_datetime__gt=current_time,admin_approval=True
  )

    return render(request, 'upcoming_auctions.html', {'upcoming_auctions': upcoming_auctions})




@login_required(login_url="/auth_app/handlelogin/")
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
            product__auction_end_datetime__lt=timezone.now() - timedelta(hours=24)
            #product__auction_end_datetime__lt=timezone.now() - timedelta(minutes=3)
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
        'purchase_link': 'your_purchase_link_here',  # Replace with the actual purchase link
    })

    # Send the email using a separate thread
    email_thread = threading.Thread(target=send_email_in_thread, args=(subject, html_message, 'hsree524@gmail.com', [second_winner.email]))
    email_thread.start()

    return HttpResponse("contact second winner Success")

def send_email_in_thread(subject, message, from_email, recipient_list):
    # Send the HTML email
    send_mail(subject, strip_tags(message), from_email, recipient_list, html_message=message)




def checkout(request):
    # Fetch the user's cart items
    user_cart = Cart.objects.get(user=request.user)
    cart_items = CartItems.objects.filter(cart=user_cart)
    total_amount = sum(item.product.current_highest_bid for item in cart_items)

    user = request.user

    # Check if the user already has an address
    try:
        address = Address.objects.get(user=user)
    except Address.DoesNotExist:
        address = None

    if request.method == 'POST':
        # Handle form submission
        name = request.POST.get('name', '')
        mobile = request.POST.get('mobile', '')
        pincode = request.POST.get('pincode', '')
        locality = request.POST.get('locality', '')
        address_text = request.POST.get('address', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        landmark = request.POST.get('landmark', '')
        

        if address:
            # Update existing address
            address.name = name
            address.mobile = mobile
            address.pincode = pincode
            address.locality = locality
            address.address = address_text
            address.city = city
            address.state = state
            address.landmark = landmark
           
            
            address.save()
        else:
            # Create a new address
            Address.objects.create(
                user=user,
                name=name,
                mobile=mobile,
                pincode=pincode,
                locality=locality,
                address=address_text,
                city=city,
                state=state,
                landmark=landmark,
               
            )
    


    return render(request, 'customer/checkout.html', {'total_amount': total_amount,'address': address})





















# from django.shortcuts import render
# from django.core.mail import send_mail
# from django.template.loader import render_to_string
# from django.utils.html import strip_tags
# from django.http import HttpResponse
# from django.contrib.auth.decorators import login_required
# from .models import Bid, AddProduct, User
# from django.core.mail import send_mail
# import threading

# @login_required
# def contact_second_winner(request, product_id, second_winner_id):
#     try:
#         product = AddProduct.objects.get(pk=product_id)
#         second_winner = User.objects.get(pk=second_winner_id)
#     except (AddProduct.DoesNotExist, User.DoesNotExist):
#         return HttpResponse("Invalid product or second winner ID")

#     # Compose the email content
#     subject = f"Congratulations! You are the Second Winner for {product.product_name}"
#     message = f"Dear {second_winner.username},\n\n" \
#               f"Congratulations! You are the Second Winner for the product '{product.product_name}'.\n" \
#               f"The auction started on {product.auction_start_datetime} and ended on {product.auction_end_datetime}.\n" \
#               f"You can purchase the product now.\n\n" \
#               f"Product Image: {product.image1.url}\n\n" \
#               f"Thank you for participating!\n\n" \
#               f"Best regards,\nThe Auction Team"

#     # Start a new thread to send the email
#     email_thread = threading.Thread(target=send_email_in_thread, args=(subject, message, 'hsree524@gmail.com', [second_winner.email]))
#     email_thread.start()

#     # Join the thread to ensure it completes before returning the HttpResponse
#     email_thread.join()

#     return HttpResponse("Success")


# def send_email_in_thread(subject, message, from_email, recipient_list):
#     send_mail(subject, message, from_email, recipient_list)