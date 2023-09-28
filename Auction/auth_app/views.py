from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import User
from django.contrib.auth import authenticate, login

# Create your views here.



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
              #make the user inactive  user.is_active=False
            user.save()
            return HttpResponse("customer sign up sucessfully")
    return render(request,'auth/signup.html')
        





def handlelogin(request):
     if request.method=="POST":
            username=request.POST['email']
            password=request.POST['password']
            myuser=authenticate(request,username=username,password=password)
            

            if myuser is not None:
                   login(request,myuser)
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