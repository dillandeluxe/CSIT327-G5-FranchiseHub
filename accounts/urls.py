# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('browse/', views.browse, name='browse'),
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('franchise/<int:franchise_id>/', views.franchise_detail, name='franchise_detail'),
    path('franchise/inquiry/', views.franchise_inquiry, name='franchise_inquiry'),
]

