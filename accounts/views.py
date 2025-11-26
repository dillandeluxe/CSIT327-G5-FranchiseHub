from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django import forms
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.http import JsonResponse

from .models import Franchisee, Franchisor, Franchise, FranchiseApplication
from .forms import FranchiseForm, FranchiseApplicationForm
from accounts.utils import get_user_role

import json
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.contrib.auth.decorators import user_passes_test
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
            messages.success(request, f"Welcome back, {username}!")  # ✅ Success message

            if user.is_superuser:
                return redirect('admin_dashboard')
            elif Franchisee.objects.filter(user=user).exists():
                return redirect('franchisee_dashboard')
            elif Franchisor.objects.filter(user=user).exists():
                return redirect('franchisor_dashboard')
            else:
                messages.error(request, "No role assigned to this user.")  # ✅ Error message
                logout(request)
                return redirect('login')
        else:
            messages.error(request, "Invalid username or password.")  # ✅ Error message
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
    q = request.GET.get('q', '').strip()
    qs = Franchise.objects.filter(is_active=True)
    if q:
        qs = qs.filter(
            Q(name__icontains=q) |
            Q(category__icontains=q) |
            Q(description__icontains=q) |
            Q(franchisor__company_name__icontains=q) |
            Q(franchisor__country__icontains=q)
        )
    franchises = qs.order_by('-created_at')

    # New: identify franchises the current user has already applied to
    applied_franchise_ids = []
    if Franchisee.objects.filter(user=request.user).exists():
        fe = Franchisee.objects.get(user=request.user)
        applied_franchise_ids = list(
            FranchiseApplication.objects.filter(franchisee=fe).values_list('franchise_id', flat=True)
        )

    return render(request, 'accounts/browse.html', {
        'franchises': franchises,
        'q': q,
        'applied_franchise_ids': applied_franchise_ids,  # used to toggle “Application Update”
    })


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
    """
    Displays the franchisor dashboard with:
    - All active franchises of the logged-in franchisor
    - Recent applications (latest 5)
    """
    try:
        # Get the logged-in user's franchisor profile
        franchisor = Franchisor.objects.get(user=request.user)
    except Franchisor.DoesNotExist:
        # Non-franchisor users are redirected with a message
        messages.error(request, "You are not registered as a franchisor.")
        return redirect('browse')

    # Fetch all active franchises for this franchisor
    franchises = franchisor.franchises.filter(is_active=True).order_by('-created_at')

    # Collect recent applications across all franchises
    applications = []
    for franchise in franchises:
        applications += list(franchise.applications.all().order_by('-created_at'))

    # Sort all applications by creation date descending and limit to latest 5
    applications = sorted(applications, key=lambda x: x.created_at, reverse=True)[:5]

    return render(request, 'accounts/franchisor_dashboard.html', {
        'franchises': franchises,
        'applications': applications
    })

@login_required
def add_franchise_view(request):
    """Allows franchisors to create new franchises with image upload."""
    try:
        franchisor = Franchisor.objects.get(user=request.user)
    except Franchisor.DoesNotExist:
        messages.error(request, "You are not registered as a franchisor.")
        return redirect('browse')

    if request.method == 'POST':
        form = FranchiseForm(request.POST, request.FILES)  # ✅ Include request.FILES
        if form.is_valid():
            franchise = form.save(commit=False)
            franchise.franchisor = franchisor
            franchise.save()
            messages.success(request, f"Franchise '{franchise.name}' created successfully!")
            return redirect('franchisor_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = FranchiseForm()

    return render(request, 'accounts/add_franchise.html', {'form': form})


@login_required
def delete_franchise(request, franchise_id):
    franchisor = Franchisor.objects.filter(user=request.user).first()
    if not franchisor:
        messages.error(request, "You are not registered as a franchisor.")  # ✅ Error message
        return redirect('browse')

    franchise = get_object_or_404(Franchise, id=franchise_id, franchisor=franchisor)
    franchise.is_active = False  # Soft delete
    franchise.save()

    messages.success(request, f"Franchise '{franchise.name}' removed successfully.")  # ✅ Success message
    return redirect('franchisor_dashboard')


@login_required
def edit_franchise_view(request, franchise_id):
    """Allows a franchisor to edit an existing franchise including image."""
    try:
        franchisor = Franchisor.objects.get(user=request.user)
    except Franchisor.DoesNotExist:
        messages.error(request, "You are not registered as a franchisor.")
        return redirect('browse')

    franchise = get_object_or_404(Franchise, id=franchise_id, franchisor=franchisor, is_active=True)

    if request.method == 'POST':
        form = FranchiseForm(request.POST, request.FILES, instance=franchise)  # ✅ Include request.FILES
        if form.is_valid():
            form.save()
            messages.success(request, f"Franchise '{franchise.name}' updated successfully!")
            return redirect('franchisor_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = FranchiseForm(instance=franchise)

    return render(request, 'accounts/edit_franchise.html', {'form': form, 'franchise': franchise})


@login_required
def all_applications(request):
    applications = FranchiseApplication.objects.all()  # Or filter by franchisor
    return render(request, 'accounts/all_applications.html', {'applications': applications})


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
    """Displays a specific franchise's detailed page with all information."""
    franchise = get_object_or_404(Franchise, id=franchise_id, is_active=True)
    
    # Check if current user already applied
    has_applied = False
    if Franchisee.objects.filter(user=request.user).exists():
        franchisee = Franchisee.objects.get(user=request.user)
        has_applied = FranchiseApplication.objects.filter(
            franchisee=franchisee,
            franchise=franchise
        ).exists()
    
    return render(request, 'accounts/franchise_detail.html', {
        'franchise': franchise,
        'has_applied': has_applied
    })


@login_required
def franchise_inquiry(request):
    """Handles inquiries from the modal form."""
    if request.method == 'POST':
        messages.success(request, "Your inquiry has been submitted successfully!")
        return redirect('browse')
    return render(request, 'accounts/franchise_detail_modal.html')


@login_required
def franchise_apply(request, franchise_id):
    """
    Franchisee submits an application for a franchise.
    Links FranchiseApplication to both Franchise & Franchisee.
    """
    franchise = get_object_or_404(Franchise, id=franchise_id, is_active=True)

    franchisee = Franchisee.objects.filter(user=request.user).first()
    if not franchisee:
        messages.error(request, "Only franchisees can submit applications.")
        return redirect('browse')

    if request.method == 'POST':
        form = FranchiseApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.franchise = franchise
            app.franchisee = franchisee
            app.save()
            messages.success(request, "Application submitted successfully.")
            return redirect('browse')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        initial = {
            'full_name': request.user.get_full_name() or request.user.username,
            'email': request.user.email,
        }
        form = FranchiseApplicationForm(initial=initial)

    return render(request, 'accounts/franchise_apply.html', {
        'form': form,
        'franchise': franchise
    })

@require_POST
@login_required
def application_set_status(request, application_id, status):
    """
    Franchisor updates application status (Approve / Reject).
    """
    app = get_object_or_404(FranchiseApplication, id=application_id)
    # Security: only owning franchisor may change status
    if not Franchisor.objects.filter(user=request.user, franchises__id=app.franchise.id).exists():
        messages.error(request, "Not authorized to modify this application.")
        return redirect('franchisor_dashboard')

    if status == 'approve':
        app.approve()
        messages.success(request, "Application approved.")
    elif status == 'reject':
        app.reject()
        messages.info(request, "Application rejected.")
    else:
        messages.error(request, "Invalid status action.")
    return redirect('franchisor_dashboard')

@require_POST
@login_required
def accept_application(request, pk):
    """
    Franchisor Accept flow:
    - Save approval_note (optional)
    - Set status to 'Accepted'
    """
    app = get_object_or_404(FranchiseApplication, id=pk)
    if not Franchisor.objects.filter(user=request.user, franchises__id=app.franchise_id).exists():
        messages.error(request, "Not authorized to accept this application.")  # ✅ Error message
        return redirect('franchisor_dashboard')

    note = request.POST.get('approval_note', '').strip()
    app.approval_note = note or None
    app.rejection_reason = None
    app.status = 'Accepted'
    app.save(update_fields=['approval_note', 'rejection_reason', 'status'])
    messages.success(request, f"Application from {app.full_name} has been accepted.")  # ✅ Success message
    return redirect('franchisor_dashboard')

@require_POST
@login_required
def reject_application(request, pk):
    """
    Franchisor Reject flow:
    - Require rejection_reason textarea
    - Set status to 'Rejected'
    """
    app = get_object_or_404(FranchiseApplication, id=pk)
    if not Franchisor.objects.filter(user=request.user, franchises__id=app.franchise_id).exists():
        messages.error(request, "Not authorized to reject this application.")  # ✅ Error message
        return redirect('franchisor_dashboard')

    reason = request.POST.get('rejection_reason', '').strip()
    if not reason:
        messages.warning(request, "Rejection reason is required.")  # ✅ Warning message
        return redirect('franchisor_dashboard')

    app.rejection_reason = reason
    app.approval_note = None
    app.status = 'Rejected'
    app.save(update_fields=['rejection_reason', 'approval_note', 'status'])
    messages.info(request, f"Application from {app.full_name} has been rejected.")  # ✅ Info message
    return redirect('franchisor_dashboard')

@login_required
def application_status(request):
    """
    Franchisee view to see application status.
    Optional query param ?franchise=<uuid> to view status for a specific franchise.
    """
    # must be a franchisee
    franchisee = Franchisee.objects.filter(user=request.user).first()
    if not franchisee:
        messages.error(request, "Only franchisees can view application status.")
        return redirect('browse')

    fid = request.GET.get('franchise')
    if fid:
        app = FranchiseApplication.objects.filter(franchisee=franchisee, franchise_id=fid).order_by('-created_at').first()
    else:
        app = FranchiseApplication.objects.filter(franchisee=franchisee).order_by('-created_at').first()

    if not app:
        messages.info(request, "You have not submitted any applications yet.")
        return redirect('browse')

    return render(request, 'accounts/application_status.html', {'application': app})

# =========================================================================
# 7. SUPER ADMIN DASHBOARD & ANALYTICS
# =========================================================================

def is_admin(user):
    # Checks if user is superuser OR has an AdminProfile
    return user.is_superuser

@login_required
@user_passes_test(is_admin, login_url='home') # Security: Only admins can see this
def admin_dashboard_view(request):
    # --- PART 1: DASHBOARD LIST DATA ---
    
    # 1. Pending Approvals (Franchise Applications)
    recent_approvals = FranchiseApplication.objects.filter(status='Pending').order_by('-created_at')[:5]
    
    # 2. Recent Users (Admin, Franchisee, etc)
    recent_users = User.objects.all().order_by('-date_joined')[:5]
    
    # 3. Active Franchises
    active_franchises = Franchise.objects.filter(is_active=True).order_by('-created_at')[:5]


    # --- PART 2: ANALYTICS CHART DATA ---

    # CHART 1: New Users Per Month (Bar Chart)
    # Group users by month joined
    users_by_month = User.objects.annotate(month=TruncMonth('date_joined')).values('month').annotate(count=Count('id')).order_by('month')
    
    # Prepare data lists for Chart.js
    user_chart_labels = [item['month'].strftime('%b') for item in users_by_month] # e.g. ['Jan', 'Feb']
    user_chart_data = [item['count'] for item in users_by_month]

    # CHART 2: Applications Activity (Line Chart) - Replacing "Website Traffic"
    # Since we don't track page views, we track Applications created per month
    apps_by_month = FranchiseApplication.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month')
    traffic_chart_labels = [item['month'].strftime('%b') for item in apps_by_month]
    traffic_chart_data = [item['count'] for item in apps_by_month]

    # CHART 3: Top Franchises by Popularity (Applications count) - Replacing "Sales"
    # We count how many applications each franchise has received
    popular_franchises = Franchise.objects.annotate(app_count=Count('applications')).order_by('-app_count')[:5]
    sales_chart_labels = [f.name for f in popular_franchises]
    sales_chart_data = [f.app_count for f in popular_franchises]

    context = {
        # Lists
        'recent_approvals': recent_approvals,
        'recent_users': recent_users,
        'active_franchises': active_franchises,
        
        # Charts - SEND RAW LISTS (Remove json.dumps here!)
        'user_chart_labels': user_chart_labels,
        'user_chart_data': user_chart_data,
        
        'traffic_chart_labels': traffic_chart_labels,
        'traffic_chart_data': traffic_chart_data,
        
        'sales_chart_labels': sales_chart_labels,
        'sales_chart_data': sales_chart_data,
    }

    return render(request, 'accounts/admin_dashboard.html', context)

# =========================================================================
# 8. FRANCHISEE DASHBOARD
# =========================================================================

@login_required
def franchisee_dashboard(request):
    """
    Franchisee dashboard showing all applications, including those for soft-deleted franchises.
    """
    try:
        franchisee = Franchisee.objects.get(user=request.user)
    except Franchisee.DoesNotExist:
        messages.error(request, "You are not registered as a franchisee.")
        return redirect('browse')

    # DO NOT filter by franchise.is_active - show all applications including soft-deleted
    applications = FranchiseApplication.objects.filter(franchisee=franchisee).select_related('franchise').order_by('-created_at')

    return render(request, 'accounts/franchisee_dashboard.html', {
        'applications': applications
    })

@require_POST
@login_required
def remove_application(request, pk):
    """
    Allows franchisee to remove an application from their dashboard.
    Used primarily when a franchise has been soft-deleted.
    """
    app = get_object_or_404(
        FranchiseApplication,
        id=pk,
        franchisee__user=request.user
    )
    franchise_name = app.franchise.name
    app.delete()
    messages.success(request, f"'{franchise_name}' removed from your dashboard.")  # ✅ Success message
    return redirect('franchisee_dashboard')

@login_required
def franchisor_franchise_detail(request, franchise_id):
    """
    Franchisor-specific detailed view of their own franchise.
    Shows management options and application statistics.
    """
    try:
        franchisor = Franchisor.objects.get(user=request.user)
    except Franchisor.DoesNotExist:
        messages.error(request, "You are not registered as a franchisor.")
        return redirect('browse')

    # Only show franchises owned by this franchisor
    franchise = get_object_or_404(
        Franchise, 
        id=franchise_id, 
        franchisor=franchisor,
        is_active=True
    )
    
    # Get application statistics
    applications = franchise.applications.all().order_by('-created_at')
    total_apps = applications.count()
    pending_apps = applications.filter(status='Pending').count()
    accepted_apps = applications.filter(status__in=['Accepted', 'Approved']).count()
    rejected_apps = applications.filter(status='Rejected').count()
    
    return render(request, 'accounts/franchisor_franchise_detail.html', {
        'franchise': franchise,
        'applications': applications[:10],  # Show latest 10
        'total_apps': total_apps,
        'pending_apps': pending_apps,
        'accepted_apps': accepted_apps,
        'rejected_apps': rejected_apps,
    })
