from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

# Create your views here.
@never_cache
def index(request):
    
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

@login_required
def CustomerHome(request):
    if 'username' in request.session:
        response = render(request,'customer_home.html')
        response['Cache-Control'] = 'no-store,must-revalidate'
        return response
    else:
        return redirect('handlelogin')
    #return render(request,'customer_home.html')