from django.urls import path
from . import views



urlpatterns = [ 
    path('', views.home),
    path('olakay/', views.get_user),
    path('auth-token/', views.obtain_token )

]