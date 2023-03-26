from django.shortcuts import render , redirect 
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login 
from django.contrib import messages
# Create your views here.


# @user_passes_test(lambda user: not user.is_authenticated, login_url='client:dashboard')    
def login_route(request): 
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        print(user)
        if user is not None:
            login(request, user)
            # Redirect to a success page
            return redirect(reverse('client:dashboard'))     
        else:
            # Show an error message
            messages.error(request,'Invalid login credentials' )
    return render(request, 'account/login.html')