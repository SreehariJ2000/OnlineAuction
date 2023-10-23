from django.shortcuts import render,redirect

from django.views.decorators.cache import never_cache
from django.contrib.auth import get_user_model

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



def adminreg(request):
    User = get_user_model()
    user_profiles = User.objects.filter(role='CUSTOMER')
    context = {'user_profiles': user_profiles}
    
    return render(request, 'admin.html', context)