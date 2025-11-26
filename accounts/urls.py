# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),  
    path('browse/', views.browse, name='browse'),  # ensure browse route handles search via ?q=
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('franchisor/dashboard/', views.franchisor_dashboard, name='franchisor_dashboard'),
    path('franchisor/add-franchise/', views.add_franchise_view, name='add_franchise'),
    path('franchisor/delete-franchise/<uuid:franchise_id>/', views.delete_franchise, name='delete_franchise'),
    path('franchisor/edit-franchise/<uuid:franchise_id>/', views.edit_franchise_view, name='edit_franchise'),
    path('franchise/<uuid:franchise_id>/', views.franchise_detail, name='franchise_detail'),
    path('franchisor/franchise/<uuid:franchise_id>/', views.franchisor_franchise_detail, name='franchisor_franchise_detail'),
    path('applications/', views.all_applications, name='all_applications'),
    # Application submit (Franchisee)
    path('franchise/<uuid:franchise_id>/apply/', views.franchise_apply, name='franchise_apply'),
    # Approve/Reject (Franchisor)
    path('application/<uuid:application_id>/<str:status>/', views.application_set_status, name='application_set_status'),
    # Franchisor actions (UUID PK)
    path("franchisor/application/<uuid:pk>/accept/", views.accept_application, name="accept_application"),
    path("franchisor/application/<uuid:pk>/reject/", views.reject_application, name="reject_application"),
    # Franchisee application status
    path("application/status/", views.application_status, name="application_status"),
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    # Franchisee dashboard
    path("franchisee/dashboard/", views.franchisee_dashboard, name="franchisee_dashboard"),
    path("application/remove/<uuid:pk>/", views.remove_application, name="remove_application"),
    # Forgot Password Flow (No Email)
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('forgot-password/questions/', views.forgot_password_questions_view, name='forgot_password_questions'),
    path('forgot-password/reset/', views.forgot_password_reset_view, name='forgot_password_reset'),
]
