from unicodedata import name
from django.shortcuts import render , redirect
from django.urls import reverse
from django.contrib.auth import get_user_model 
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from account.models import ExpenseRequest , Department , CustomUser
from django.views.generic import ListView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# # Create your views here.


Users = get_user_model()

def removeZero(val):
    if int(val[0]) == 0:
        return removeZero(val[1:])
    else:
        return val

# def line_executive_dashboard(request):
#     expense =  ExpenseRequest.objects.filter(is_hod=True).exclude(is_line_executive=True )
#     context = { 'expense_request': expense }
#     return render(request, 'line-executive/line-executive-dashboard.html', context )  

# def cost_management_dashboard(request):
#     expense =  ExpenseRequest.objects.filter(is_line_executive=True).exclude(is_cost_manager=True )
#     context = { 'expense_request': expense }
#     return render(request, 'cost-management-dashboard.html', context )  



def home(request):
    return render(request, 'home.html') 


@login_required
def dashboard(request):
    # user = Users.objects.get(id=1)
    user = Users.objects.get(id=request.user.id) 
    print(user.groups.all()) 
    if user.groups.filter(name='requester'):
        expense =  ExpenseRequest.objects.filter( request_user=user )
        expense =  ExpenseRequest.objects.all()    
        # expense =  ExpenseRequest.objects.filter(request_department=user.department).exclude(is_hod=True).exclude(is_rejected=True)
        context = { 'expense_request': expense }  
        # return render(request, 'head_of_department/department-hod-dashboard.html', context )
        return render(request, 'requester/dashboard.html', context)

    if user.groups.filter(name="head_of_department") or user.is_staff:   
        user = Users.objects.get(id=request.user.id)
        expense =  ExpenseRequest.objects.filter(request_department=user.department).exclude(is_hod=True).exclude(is_rejected=True)
        context = { 'expense_request': expense }
        return render(request, 'head_of_department/department-hod-dashboard.html', context )

    if user.groups.filter(name="cost_management"):
        expense =  ExpenseRequest.objects.filter(is_line_executive=True).exclude(is_cost_manager=True )
        context = { 'expense_request': expense }
        return render(request, 'cost-management-dashboard.html', context ) 
    
    if user.groups.filter(name="line_executive"):
        expense =  ExpenseRequest.objects.filter(is_hod=True).exclude(is_line_executive=True )
        context = { 'expense_request': expense }
        return render(request, 'line-executive/line-executive-dashboard.html', context )
    

    



def reject_expense_request(request, slug):
    expense = ExpenseRequest.objects.get(slug=slug)
    
    expense.reject()
    # expense.is_rejected =True
    expense.save()
    print(expense.is_rejected) 
    return HttpResponseRedirect(request.META['HTTP_REFERER'])



def accept_expense_request(request, slug):
    expense = ExpenseRequest.objects.get(slug=slug)
    user = Users.objects.get(id=request.user.id)
    if user.is_head_of_department:
        expense.is_hod =True
    elif user.is_cost_management:
        expense.is_cost_manager = True
    elif user.is_line_executive:
        expense.is_line_executive = True
    elif user.is_md:
        expense.is_md = True
        expense.is_completed = True
        expense.is_disbursed = True
    expense.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])




class RequesterListView(ListView):
    template_name = 'head_of_department/requester_list.html'
    
    def get_queryset(self):
        user_id = self.request.user.id
        user_obj = Users.objects.get(id=user_id)
        user_department = user_obj.department
        print(user_department)
        me = Group.user_set.filter(name='requester')
        print(me)
        requesters = Users.objects.filter(department=user_department)
        print(type(requesters))
        return requesters
requester_list = RequesterListView.as_view()
def add_requester(request):
    return render(request, 'head_of_department/add_requester.html') 
    

# Create your views here.





def requester_dashboard(request):
    expense =  ExpenseRequest.objects.all()
    context = { 'expense_request': expense } 
    return render(request, 'requester/requester-dashboard.html', context)






def add_request(request):
    if request.method == 'POST':
        user = Users.objects.get(id=request.user.id)
        department = Department.objects.get(name=user.department)
        price = request.POST.get('price')
        title = request.POST.get('title') 
        description = request.POST.get('description')
        if not price:
            messages.error(request,'Expense request price is required' )
            return render(request, 'requester/request-form.html')
        amount = removeZero(price)
        if not title:
            messages.error(request,'Expense request title is required' )
            return render(request, 'requester/request-form.html')
        if not description:
            messages.error(request,'Expense request description is required' )
            return render(request, 'requester/request-form.html')    
        # check if department has up to three pending expense request
        has_pending_expense_request = ExpenseRequest.objects.filter(
            is_rejected= False,
            is_completed= False,
            request_department=department
        ).count()
        if has_pending_expense_request >= 3 :
            messages.error(request,'Expense request cannot be processed, department has reach maximum pending request' )
            return render(request, 'requester/request-form.html')
        try:
            ExpenseRequest.objects.create(
                request_user=user, 
                title=title ,
                request_department=department , 
                description=description , 
                amount=amount
            )
            return redirect(reverse('client:dashboard'))
        except:
            messages.error(request,'There is an error saving request' )
    return render(request, 'requester/request-form.html')







def expense_history(request):
    expense = ExpenseRequest.objects.filter(is_completed=True)
    context = { 'expense_request': expense } 
    return render(request, 'requester/request-history.html', context)







