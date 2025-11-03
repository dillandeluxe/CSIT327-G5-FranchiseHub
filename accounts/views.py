from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django import forms

from .models import Franchisee, Franchisor, Franchise
from .forms import FranchiseForm
from accounts.utils import get_user_role


# =========================================================================
# 1. AUTHENTICATION VIEWS
# =========================================================================

def register_view(request):
    """Handles new user registration for Franchisees and Franchisors."""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        try:
            with transaction.atomic():
                user = User.objects.create_user(username=username, email=email, password=password)

                if role == 'franchisor':
                    Franchisor.objects.create(user=user)
                elif role == 'franchisee':
                    Franchisee.objects.create(user=user)
                else:
                    messages.error(request, "Invalid role selected.")
                    return redirect('register')

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)

            # Redirect based on role
            if role == 'franchisee':
                return redirect('browse')
            elif role == 'franchisor':
                return redirect('franchisor_dashboard')
            else:
                return redirect('home')

        except Exception as e:
            messages.error(request, f"Error during registration: {str(e)}")
            return redirect('register')

    return render(request, 'accounts/register.html')


def login_view(request):
    """Handles user authentication and redirects based on role."""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {username}!")

            if Franchisee.objects.filter(user=user).exists():
                return redirect('browse')
            elif Franchisor.objects.filter(user=user).exists():
                return redirect('franchisor_dashboard')
            else:
                messages.error(request, "No role assigned to this user.")
                return redirect('login')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'accounts/login.html')


def logout_view(request):
    """Logs out the user."""
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


# =========================================================================
# 2. MAIN APP VIEWS
# =========================================================================

def home_view(request):
    """Landing page."""
    return render(request, 'accounts/home.html')


@login_required
def browse(request):
    """Displays all active franchises for franchisees."""
    franchises = Franchise.objects.filter(is_active=True)
    return render(request, 'accounts/browse.html', {'franchises': franchises})


# =========================================================================
# 3. PROFILE VIEW
# =========================================================================

class ProfileForm(forms.ModelForm):
    """Simple form for editing user info."""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


@login_required
def profile_view(request):
    """Displays and allows editing of the user's profile."""
    user = request.user

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        form = ProfileForm(instance=user)

    return render(request, 'accounts/profile.html', {'form': form})


# =========================================================================
# 4. FRANCHISOR DASHBOARD + ADD FRANCHISE
# =========================================================================

@login_required
def franchisor_dashboard(request):
    """Displays franchisor dashboard with their franchises."""
    try:
        franchisor = Franchisor.objects.get(user=request.user)
    except Franchisor.DoesNotExist:
        messages.error(request, "You are not registered as a franchisor.")
        return redirect('browse')

    franchises = Franchise.objects.filter(franchisor=franchisor)
    return render(request, 'accounts/franchisor_dashboard.html', {
        'franchises': franchises
    })


@login_required
def add_franchise_view(request):
    """Allows franchisors to create new franchises (Add Franchise button)."""
    if not request.user.is_authenticated:
        return redirect('login')

    franchisor = Franchisor.objects.filter(user=request.user).first()
    if not franchisor:
        messages.error(request, "You are not registered as a franchisor.")
        return redirect('browse')

    if request.method == 'POST':
        form = FranchiseForm(request.POST)
        if form.is_valid():
            franchise = form.save(commit=False)
            franchise.franchisor = franchisor
            franchise.save()
            messages.success(request, "Franchise created successfully!")
            return redirect('franchisor_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = FranchiseForm()

    return render(request, 'accounts/add_franchise.html', {'form': form})


# =========================================================================
# 5. ROLE DASHBOARD REDIRECT
# =========================================================================

@login_required
def dashboard_redirect(request):
    """Redirects users to their appropriate dashboard."""
    user_role = get_user_role(request.user)
    if user_role == 'franchisor':
        return redirect('franchisor_dashboard')
    return redirect('browse')


# =========================================================================
# 6. FRANCHISE DETAIL + INQUIRY
# =========================================================================

@login_required
def franchise_detail(request, franchise_id):
    """Displays a specific franchise’s detailed page."""
    franchise = get_object_or_404(Franchise, id=franchise_id)
    return render(request, 'accounts/franchise_detail.html', {'franchise': franchise})


@login_required
def franchise_inquiry(request):
    """Handles inquiries from the modal form."""
    if request.method == 'POST':
        messages.success(request, "Your inquiry has been submitted successfully!")
        return redirect('browse')
    return render(request, 'accounts/franchise_detail_modal.html')
