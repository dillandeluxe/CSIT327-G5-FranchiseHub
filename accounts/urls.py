# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),  
    path('browse/', views.browse, name='browse'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('franchisor/dashboard/', views.franchisor_dashboard, name='franchisor_dashboard'),
    path('franchisor/add-franchise/', views.add_franchise_view, name='add_franchise'),



]
