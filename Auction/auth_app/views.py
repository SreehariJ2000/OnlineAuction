from django.shortcuts import render

# Create your views here.
def Sign_up(request):
    return render(request,'auth/signup.html')