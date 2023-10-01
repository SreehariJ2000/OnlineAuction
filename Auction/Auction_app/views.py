from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    return render(request,'index.html')

@login_required(login_url="/auth_app/handlelogin")
def CustomerHome(request):
    return render(request,'customer_home.html')