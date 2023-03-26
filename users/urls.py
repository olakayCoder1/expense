from django.urls import path
from . import views



app_name='users'

urlpatterns = [ 
    path('', views.users_list, name='users'), 
    path('add', views.user_add, name='user-add'), 
    path('<str:slug>', views.user_profile, name='user-profile'), 
] 