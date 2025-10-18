from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.contrib.auth.decorators import login_required # <-- New Import for security


# =========================================================================
# 1. AUTHENTICATION VIEWS
# =========================================================================

def register_view(request):
    """Handles user registration and associated profile creation (Franchisee/Franchisor)."""

    from .models import Franchisee, Franchisor  # Importing here to avoid circular imports
    if request.method == 'POST':
        # 1. Get ALL necessary data from the POST request
        username = request.POST.get('username').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role')

        # Basic Validation Checks
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')
        
        if not email:
            messages.error(request, "Email is required.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        # Use transaction.atomic for database consistency
        try:
            with transaction.atomic():
                # 2. Create the base Django User
                user = User.objects.create_user(
                    username=username, 
                    email=email, 
                    password=password
                )
                user.save()

                # 3. Create the corresponding profile based on role
                if role == 'franchisee':
                    Franchisee.objects.create(
                        user=user, 
                        business_name=f"New Franchisee ({username})"
                    )
                elif role == 'franchisor':
                    Franchisor.objects.create(
                        user=user, 
                        company_name=f"New Franchisor ({username})", 
                        email=email
                    )
                else:
                    raise ValueError("Invalid role selected.")
                    
                # 4. Log the user in and redirect to the browse page
                login(request, user)
                messages.success(request, f"Welcome to FranchiseHub, {username}!")
                return redirect('browse')

        except Exception as e:
            messages.error(request, f"Registration failed due to an error. Please try again. (Details: {e})")
            return redirect('register')

    return render(request, 'accounts/register.html')


def login_view(request):
    """Handles user authentication."""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Successful authentication: Log the user in and redirect to browse
            login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            return redirect('browse') 
        else:
            # Failed authentication: Display error message
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'accounts/login.html')


def logout_view(request):
    """Logs the user out and redirects to the login page."""
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


# =========================================================================
# 2. APPLICATION VIEWS
# =========================================================================

def home_view(request):
    """The main landing page view."""
    return render(request, 'accounts/home.html')


@login_required # <-- Security: Only logged-in users can access this page
def browse(request):
    """The main view for displaying franchise opportunities."""
    return render(request, 'accounts/browse.html')

# NOTE: The provided code does not include the AdminProfile logic, 
# but the foundation is ready for expansion if needed later.
