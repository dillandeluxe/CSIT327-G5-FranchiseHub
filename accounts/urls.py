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
    # ✅ About, Support, and Privacy page routes
    path('about/', views.about_view, name='about'),
    path('support/', views.support_view, name='support'),
    path('privacy/', views.privacy_view, name='privacy'),
    # ✅ NOTIFICATION ROUTES
    path('notifications/', views.notifications_view, name='notifications'),
    path('notifications/api/', views.get_notifications_api, name='notifications_api'),
    path('notifications/<uuid:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/mark-all-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
    # ✅ CUSTOM ADMIN FRANCHISE MANAGEMENT
    path('admin/franchises/', views.admin_franchise_management, name='admin_franchise_management'),
    path('admin/franchise/<uuid:franchise_id>/', views.admin_franchise_detail, name='admin_franchise_detail'),
    path('admin/franchise/<uuid:franchise_id>/approve/', views.admin_approve_franchise, name='admin_approve_franchise'),
    path('admin/franchise/<uuid:franchise_id>/reject/', views.admin_reject_franchise, name='admin_reject_franchise'),
    # ✅ NEW: Permanent delete routes for admin
    path('admin/franchise/permanent-delete/<uuid:franchise_id>/', views.admin_permanent_delete_franchise, name='admin_permanent_delete_franchise'),
    path('admin/franchise/permanent-delete-all/', views.admin_permanent_delete_all_franchises, name='admin_permanent_delete_all_franchises'),
    # ✅ NEW: Favorites/Watchlist Routes
    path('favorites/', views.favorites_view, name='favorites'),
    path('favorites/toggle/<uuid:franchise_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/check/<uuid:franchise_id>/', views.check_favorite, name='check_favorite'),
    # Real-time stats endpoint
    path('franchisor/dashboard-stats/', views.dashboard_stats, name='dashboard_stats'),
    # ✅ CUSTOM ADMIN URLS
    path('system-admin/', views.admin_index, name='admin_index'),
    path('system-admin/users/', views.admin_user_list, name='admin_user_list'),
    path('system-admin/users/add/', views.admin_add_user, name='admin_add_user'),
    path('system-admin/users/<int:user_id>/change/', views.admin_change_user, name='admin_change_user'),
    path('system-admin/users/<int:user_id>/delete/', views.admin_delete_user, name='admin_delete_user'),
    path('system-admin/password_change/', views.admin_password_change, name='admin_password_change'),
]
