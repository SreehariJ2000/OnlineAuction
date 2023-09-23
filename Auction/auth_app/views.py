from django.shortcuts import render
from django.contrib import messages

# Create your views here.
def Sign_up(request):
    if request.method=='POST':
        fname=request.POST['first_name']
        lname=request.POST['last_name']
        Email=request.POST['email']
        Username=Email
        Password=request.POST['password']                                  
        Password1=request.POST['confirm_password']
       
    return render(request,'auth/signup.html')
