from django.shortcuts import render,redirect
from  auth_app.models import User
from django.db.models import Q
from django.views.decorators.cache import never_cache
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
# Create your views here.
@never_cache
def index(request):
    
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')


def CustomerHome(request):
    if 'username' in request.session:
        response = render(request,'customer_home.html')
        response['Cache-Control'] = 'no-store,must-revalidate'
        return response
    else:
        return redirect('handlelogin')
    #return render(request,'customer_home.html')



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





def add_product(request):
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
        

        # Create a new AddProduct instance and save it
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
            seller=request.user.sellerprofile  # You may need to customize this part
        )
        add_product.save()
        messages.success(request,"waiting for approval")
        return redirect('/add_product')  
    return render(request,'sellor/add_product.html')





def get_categories(request):
    categories = Category.objects.values('id', 'cat_name')
    return JsonResponse({'categories': list(categories)})


def get_subcategories(request):
    category_id = 1  # You may pass category_id as a query parameter
    cat = Category.objects.all()
    subc = []
    for category in cat:
        subcategories = SubCategory.objects.filter(category_id=category.pk)
        subcategories_list = list(subcategories.values())  # Convert queryset to a list of dictionaries
        subc.append({'category': category.cat_name, 'subcategories': subcategories_list})
    return JsonResponse({'categories_and_subcategories': subc})



def product_approval(request):
    unapproved_products = AddProduct.objects.filter(admin_approval=False)
    
    return render(request,'admin/pending_product.html',{'unapproved_products': unapproved_products})



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

    return render(request, 'customer_home.html', {'live_auctions': live_auctions})

def upcoming_auctions(request):
    
    current_time = timezone.now()
    upcoming_auctions = AddProduct.objects.filter(
    auction_start_datetime__gt=current_time,admin_approval=True
  )

    return render(request, 'upcoming_auctions.html', {'upcoming_auctions': upcoming_auctions})



def bidding(request,product_id):
    user = request.user
    product = AddProduct.objects.get(id=product_id)
    list=Bid.objects.filter(product_id=product_id)
    context = {
        'product': product,
        'user_data': user,
        'list':list
    }
    return render(request,'customer/bidding.html',context)


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

        if bid_amount > product.current_highest_bid:
            product.current_highest_bid = bid_amount
            product.save()

            Bid.objects.create(product=product, bidder=request.user, bid_amount=bid_amount)
        
            return redirect('bidding', product_id=product_id)
        else:
            messages.success(request," use higher amount than now ")
            return redirect('bidding', product_id=product_id)
            

     
