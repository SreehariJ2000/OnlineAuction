from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from .models import User
from django.contrib.auth import authenticate, login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
#from django.utils.encoding import DjangoUnicodeDecodeError


from django.views.generic import View
from .utils import *

#for activating user account
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from django.template.loader import render_to_string
#from django.urls import NoReverseMatch,reverse
# Create your views here.

#email
#from django.core.mail import send_mail,EmailMultiAlternatives
#from django.core.mail import BadHeaderError,send_mail
#from django.core import mail
from django.conf import settings
from django.core.mail import EmailMessage

#threading
import threading

#reset passwor generater
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class EmailThread(threading.Thread):
       def __init__(self, email_message):
              super().__init__()
              self.email_message=email_message
       def run(self):
              self.email_message.send()


def Sign_up(request):
    if request.method=="POST":
            fname=request.POST['first_name']
            lname=request.POST['last_name']
            email=request.POST['email']
            username=email
            password=request.POST['password']
            confirm_password=request.POST['confirm_password']
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
            current_site=get_current_site(request)   #get link of site
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
                        #request.session['username'] =myuser.username
                   if myuser.role=='CUSTOMER':
                        messages.success(request,"Login Sucess!!!")
                        return redirect('/customerhome')
                   elif myuser.role=='SELLER':
                        messages.success(request,"Login Sucess!!!")
                        return HttpResponse("seller login")
                   elif myuser.role=='ADMIN':
                          messages.success(request,"Login Sucess!!!")
                          return HttpResponse("Admin login ")
                          
            else:
                   messages.error(request,"Some thing went wrong")
                   return redirect('/auth_app/handlelogin')
     return render(request,'auth/login.html')


def handlelogout(request):
    if request.user.is_authenticated:
        logout(request)

    # Redirect to the login page or any other page you prefer
    return redirect('/') 