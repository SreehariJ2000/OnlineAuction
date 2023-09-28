from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'index.html')


def CustomerHome(request):
    return render(request,'customer_home.html')