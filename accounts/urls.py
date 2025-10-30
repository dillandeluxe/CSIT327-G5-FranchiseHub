# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),  
    path('browse/', views.browse, name='browse'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # NEW Read-only profile view (default: my-profile)
    path('profile/', views.profile_view, name='profile'), 
    # RENAMED Edit profile view
    path('edit-profile/', views.edit_profile_view, name='edit_profile'),
]
