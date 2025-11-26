from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse
from accounts.models import AdminProfile
from django.utils.deprecation import MiddlewareMixin

class AdminAuthorizationMiddleware:
    """
    Custom middleware that restricts access to /admin/* routes.
    Only users with an AdminProfile can access them.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Allow access to the built-in Django admin (it uses /admin/)
        if request.path.startswith(reverse('admin:index')):
            return self.get_response(request)

        # Custom route restriction: e.g. /admin/users, /admin/dashboard, etc.
        if request.path.startswith('/admin/') and not request.path.startswith('/admin/login'):
            # Check if the user is authenticated and has an AdminProfile
            if request.user.is_authenticated:
                is_admin = AdminProfile.objects.filter(user=request.user).exists()
                if not is_admin:
                    return HttpResponseForbidden("403 Forbidden: You do not have permission to access this page.")
            else:
                # Not logged in — redirect to login
                return redirect('/login/')

        return self.get_response(request)

class NoCacheMiddleware(MiddlewareMixin):
    """
    Middleware to prevent caching of authenticated pages.
    This ensures users can't go back to authenticated pages after logout.
    """
    def process_response(self, request, response):
        # Only apply to authenticated users
        if request.user.is_authenticated:
            # Prevent caching of all authenticated pages
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private, max-age=0'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        return response
