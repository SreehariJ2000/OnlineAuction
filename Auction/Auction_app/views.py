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



def add_product(request):
    if request.method == 'POST':
        # Retrieve data from the form
        category = request.POST.get('category')
        sub_category = request.POST.get('sub_category')
        print(category,sub_category,"11111111111111111111111111111111111")
        product_name = request.POST.get('product_name')
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
        return HttpResponse("success")  
    return render(request,'sellor/add_product.html')





def get_categories(request):
    categories = Category.objects.values('id', 'cat_name')
    return JsonResponse({'categories': list(categories)})

from django.db import connection
def get_subcategories(request):
    category_id = 1  # You may pass category_id as a query parameter
    cat = Category.objects.all()
    subc = []
    for category in cat:
        subcategories = SubCategory.objects.filter(category_id=category.pk)
        subcategories_list = list(subcategories.values())  # Convert queryset to a list of dictionaries
        subc.append({'category': category.cat_name, 'subcategories': subcategories_list})
    return JsonResponse({'categories_and_subcategories': subc})




