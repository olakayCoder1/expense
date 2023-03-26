from django.shortcuts import render
from account.models import  CustomUser , Role , Department
from django.contrib import messages
from django.contrib.auth.models import Group
# Create your views here.




def users_list(request): 
    users = CustomUser.objects.all()
    context = { 'users': users } 
    return render(request, 'users/list.html', context)


def user_add(request): 
    departments = Department.objects.all()
    roles = Role.objects.all()
    context = { 
        'roles': roles,
        'departments':departments 
    } 
    if request.method == 'POST' : 
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        department = request.POST.get('department') 
        role = request.POST.get('role') 
        print(request.POST) 
        
        if not first_name:
            messages.error(request, 'First name is a required field')
            return render(request, 'users/add.html', context)
        if not last_name:
            messages.error(request, 'Last name is a required field')
            return render(request, 'users/add.html', context)
        if not email:
            messages.error(request, 'Email  is a required field')
            return render(request, 'users/add.html', context)
        if not department:
            messages.error(request, 'Department is a required field')
            return render(request, 'users/add.html', context)
    
        #  check if email already exist
        if CustomUser.is_email_exist(email):
            messages.error(request, 'Email already exist')
            return render(request, 'users/add.html', context)
        
        department = Department.objects.get(id=department)
        role = Role.objects.get(name=role)
        user = CustomUser.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password = first_name,
            department=department,
            role=role

        )        
    users = CustomUser.objects.all()
    
     
    return render(request, 'users/add.html', context)


def user_profile(request, slug ): 
    
    user = CustomUser.objects.get(id=1)

    context = { 
        'user': user,
    } 
    return render(request, 'users/profile.html', context)
