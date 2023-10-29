from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import User
from django.contrib.auth import authenticate, login,logout
from django.utils.encoding import DjangoUnicodeDecodeError
import re

from django.views.generic import View
from .utils import *

#for activating user account
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from django.template.loader import render_to_string

# Create your views here.

#email
from django.conf import settings
from django.core.mail import EmailMessage

#threading
import threading

#reset passwor generater
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .models import *
from django.views import View
from .models import *



class EmailThread(threading.Thread):
       def __init__(self, email_message):
              super().__init__()
              self.email_message=email_message
       def run(self):
              self.email_message.send()





def is_valid_email(email):
    email_pattern = r'^[a-z0-9]+@[a-z0-9.-]+\.[a-z]+$'
    return re.match(email_pattern, email) is not None




def Sign_up(request):
    if request.method=="POST":
            fname=request.POST['first_name']
            lname=request.POST['last_name']
            email=request.POST['email']
            username=email
            password=request.POST['password']
            confirm_password=request.POST['confirm_password']

            if not is_valid_email(email):
                  messages.warning(request,"enter a valid email")
                  return render(request,'auth/signup.html')

            
            if password!=confirm_password:
                    messages.warning(request,"password is not matching")
                    return render(request,'auth/signup.html')
            try:
                      if User.objects.get(username=email):
                             messages.warning(request,"Email is already taken")
                             return render(request,'auth/signup.html')
            except Exception as identifiers:
                      pass

            user=User.objects.create_user(first_name=fname,last_name=lname,email=email,password=password,username=username,role='CUSTOMER')
            user.is_active=False  #make the user inactive
            user.save()
            current_site=get_current_site(request)  
            email_subject="Activate your account"
            message=render_to_string('auth/activate.html',{
                   'user':user,
                   'domain':current_site.domain,
                   'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                   'token':generate_token.make_token(user)


            })

            email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email],)
            EmailThread(email_message).start()
            messages.info(request,"Active your account by clicking the link send to your email")



           
            return redirect('/auth_app/handlelogin/')
            
             
            
    return render(request,'auth/signup.html')
        

class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as identifier:
            user=None
        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            messages.info(request,"Account activated sucessfully")
            return redirect('/auth_app/handlelogin/')
        return render(request,"auth/activatefail.html")





def handlelogin(request):
     if request.method=="POST":
            username=request.POST['email']
            password=request.POST['password']
            myuser=authenticate(request,username=username,password=password)
            

            if myuser is not None:
                   login(request,myuser)
                   request.session['username']=username
                        #request.session['username'] =myuser.username
                   if myuser.role=='CUSTOMER':
                        
                        return redirect('/customerhome')
                   elif myuser.role=='SELLER':
                        
                        return redirect('seller_dashboard')
                   elif myuser.role=='ADMIN':
                          
                          return redirect('/adminreg')
                          
            else:
                   messages.error(request,"enter valid credentials")
                   return redirect('/auth_app/handlelogin')
     response = render(request,'auth/login.html')
     response['Cache-Control'] = 'no-store,must-revalidate'
     return response
    
    # return render(request,'auth/login.html')



#reset password
class RequestResetEmailView(View):
      def get(self,request):
            return render(request,'auth/request-reset-email.html')
      
      def post(self,request):
            email=request.POST['email']
            user=User.objects.filter(email=email)

            if user.exists():
                  current_site=get_current_site(request)
                  email_sub="[Reset your Password]"
                  message=render_to_string('auth/reset-user-password.html',{
                        
                        'domain':current_site.domain,
                        'uid':urlsafe_base64_encode(force_bytes(user[0].pk)),
                        'token':PasswordResetTokenGenerator().make_token(user[0])
                  })

                  email_message=EmailMessage(email_sub,message,settings.EMAIL_HOST_USER,[email])
                  EmailThread(email_message).start()
                  messages.info(request,"we sent instructions to how reset password")
                  return render(request,'auth/request-reset-email.html')



            
class SetNewPassword(View):
       def get(self,request,uidb64,token):
              
              context={
                  'uidb64':uidb64,
                  'token':token
               }
              try:
                  user_id=force_str(urlsafe_base64_decode(uidb64))
                  user=User.objects.get(pk=user_id)
                  if not PasswordResetTokenGenerator().check_token(user,token):
                        messages.warning(request,"password reset link is in valid")
                        return render(request,'auth/request-reset-email.html')
              except DjangoUnicodeDecodeError as identifier:
                    pass

              return render(request,'auth/set-new-password.html',context)
      
       def post(self,request,uidb64,token):
              context={
                   'uidb64':uidb64,
                  'token':token
              
                }
              password=request.POST['password']
              confirm_password=request.POST['confirm_password']
              if password!=confirm_password:
                    messages.warning(request,"password is not matching")
                    return render(request,'auth/set-new-password.html',context)
              try:
                    user_id=force_str(urlsafe_base64_decode(uidb64))
                    user=User.objects.get(pk=user_id)
                    user.set_password(password)
                    user.save()
                    messages.success(request,"Password reset sucess. you can login with new password")
                    return redirect('/auth_app/handlelogin/')
              
              except DjangoUnicodeDecodeError as identifier:
                    messages.error(request,"Something went wrong")
                    return redirect('auth/set-new-password.html',context)
              return render(request,'auth/set-new-password.html',context)


       







def handlelogout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('handlelogin')




  # Import your Profile model

def update_profile(request):
    if request.method == 'POST':
        # Process the form data and update the user's profile
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        bidder_id = request.POST['bidder_id']
        if User.objects.filter(username=email).exclude(id=request.user.id).exists():
            messages.warning(request, "Email is already taken")
            return redirect('update-profile')  # Redirect to the same page with the warning message

        # Validate phone
        if Profile.objects.filter(phone=phone).exclude(user=request.user).exists():
            messages.warning(request, "Phone number is already taken")
            return redirect('update-profile')  # Redirect to the same page with the warning message

        # Validate bidder username
        if Profile.objects.filter(bidder_id=bidder_id).exclude(user=request.user).exists():
            messages.warning(request, "Bidder Username is already taken")
            return redirect('update-profile')
        
        if email != request.user.email:
            user=request.user
            user.email=email
            user.username=email
            user.is_active=False  #make the user inactive
            user.save()
            
            
            current_site=get_current_site(request)  
            email_subject="Activate your account"
            message=render_to_string('auth/activate.html',{
                   'user':user,
                   'domain':current_site.domain,
                   'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                   'token':generate_token.make_token(user)


            })

            email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email],)
            EmailThread(email_message).start()
            messages.info(request,"Active your account by clicking the link send to your email")
            logout(request)
           
            return redirect('/auth_app/handlelogin/')
            
        
        # Update the User model fields
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.username=email
        user.email = email
        user.save()
        
        # Update the Profile model fields
        profile, created = Profile.objects.get_or_create(user=user)
        profile.phone = phone
        profile.bidder_id = bidder_id
        profile.save()
        
        # Logout the user and redirect to the signup page
        messages.success(request,'profile updated')
        return redirect('update-profile')
    else:
        return render(request, 'auth/update_profile.html', {'user': request.user})


  



  #sellor reisteration



def sellor_signup(request):
    if request.method=="POST":
            fname=request.POST['first_name']
            lname=request.POST['last_name']
            email=request.POST['email']
            username=email
            password=request.POST['password']
            confirm_password=request.POST['confirm_password']

            if not is_valid_email(email):
                  messages.warning(request,"enter a valid email")
                  return render(request,'auth/sellor_signup.html')

            
            if password!=confirm_password:
                    messages.warning(request,"password is not matching")
                    return render(request,'auth/sellor_signup.html')
            try:
                      if User.objects.get(username=email):
                             messages.warning(request,"Email is already taken")
                             return render(request,'auth/sellor_signup.html')
            except Exception as identifiers:
                      pass

            user=User.objects.create_user(first_name=fname,last_name=lname,email=email,password=password,username=username,role='SELLER')
            user.is_active=False  #make the user inactive
            user.save()

            try:
                  seller_profile=user.sellerprofile
            except SellerProfile.DoesNotExist:
                  seller_profile=SellerProfile(user=user)
                  seller_profile.save()
            
            current_site=get_current_site(request)  
            email_subject="Activate your account"
            message=render_to_string('auth/activate.html',{
                   'user':user,
                   'domain':current_site.domain,
                   'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                   'token':generate_token.make_token(user)


            })

            email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email],)
            EmailThread(email_message).start()
            messages.info(request,"Active your account by clicking the link send to your email")



           
            return redirect('/auth_app/handlelogin/')
            
             
            
    return render(request,'auth/sellor_signup.html')
 




 
def seller_dashboard(request):
    if request.user.sellerprofile.is_approved:
        return render(request, 'sellor/sellor_dashboard.html')
    else:
        messages.success(request, 'Your profile is pending admin approval.')
        return render(request, 'auth/sellor_update_profile.html')
    




def create_seller_profile(request):
    if request.method == 'POST':
        user = request.user
        
        phone = request.POST.get('phone')
        profile_picture = request.FILES.get('profile_picture')
        pin = request.POST.get('pin')
        address = request.POST.get('address')
        state = request.POST.get('state')
        country = request.POST.get('country')
        city = request.POST.get('city')
       
        gender = request.POST.get('gender')
        
        
        

        # Check if a SellerProfile already exists for the user
        seller_profile, created = SellerProfile.objects.get_or_create(user=user, defaults={
            'phone': phone,
            'profile_picture': profile_picture,
            'pin': pin,
            'address': address,
            'state': state,
            'country': country,
            'city': city,
            'gender': gender,
        })

        if not created:
            # Update the fields if the profile already exists
            seller_profile.phone = phone
            seller_profile.profile_picture = profile_picture
            seller_profile.pin = pin
            seller_profile.address = address
           
            seller_profile.gender = gender
            if country:
                seller_profile.country = country
            if state:
                seller_profile.state = state
            if city:
                seller_profile.city = city
            seller_profile.save()

        messages.success(request, 'Your seller profile has been submitted for approval.')
        return redirect('create_seller_profile')

    return render(request, 'auth/sellor_update_profile.html')
