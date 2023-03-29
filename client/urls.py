from django.urls import path
from . import views



app_name = 'client'

urlpatterns = [ 
    path('', views.home, name='home'), 
    path('dashboard', views.dashboard, name='dashboard'),
    path('expenses/create', views.add_request , name='create_request'),
    path('expenses', views.expense_history , name='expense-history'),
    path('expenses/<str:slug>', views.expense_detail , name='expense-detail'),
    path('requesters', views.requester_list, name='requester_list'),
    # path('dashboard/cost-management/', views.cost_management_dashboard, name='cost-management-dashboard'),
    # path('dashboard/head-of-department/', views.hod_dashboard, name='hod-dashboard'),
    path('reject_expense_request/<str:slug>', views.reject_expense_request, name='reject_expense_request'),
    path('accept_expense_request/<str:slug>', views.accept_expense_request, name='accept_expense_request'),
    path('head-of-department/requester/create', views.add_requester, name="add_requester"),
] 