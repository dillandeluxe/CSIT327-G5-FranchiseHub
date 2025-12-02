from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django import forms
from django.views.decorators.http import require_POST, require_http_methods
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from .models import (
    Franchisee, 
    Franchisor, 
    Franchise, 
    FranchiseApplication,  # ✅ Make sure this is imported
    SecurityQuestion, 
    Profile, 
    Notification,
    UserFavorites  # ✅ Add this to imports
)
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
    """Handles new user registration with security questions."""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role')
        
        # Security question answers
        answer1 = request.POST.get('security_answer_1', '').strip()
        answer2 = request.POST.get('security_answer_2', '').strip()
        answer3 = request.POST.get('security_answer_3', '').strip()

        # Validation
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        # Validate security answers
        if not all([answer1, answer2, answer3]):
            messages.error(request, "All security questions must be answered.")
            return redirect('register')

        if len(answer1) < 2 or len(answer2) < 2 or len(answer3) < 2:
            messages.error(request, "Security answers must be at least 2 characters.")
            return redirect('register')

        try:
            with transaction.atomic():
                # Create user
                user = User.objects.create_user(username=username, email=email, password=password)

                # Create security questions
                sec_q = SecurityQuestion.objects.create(user=user)
                sec_q.set_answer(1, answer1)
                sec_q.set_answer(2, answer2)
                sec_q.set_answer(3, answer3)
                sec_q.save()

                # Create role profile
                if role == 'franchisor':
                    Franchisor.objects.create(user=user, company_name=username)
                elif role == 'franchisee':
                    Franchisee.objects.create(user=user, business_name=username)
                else:
                    messages.error(request, "Invalid role selected.")
                    return redirect('register')

            # Auto-login
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)

            messages.success(request, f"Account created successfully! Welcome, {username}.")
            
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

            # ✅ PREVENT BROWSER BACK BUTTON FROM LOGGING OUT
            # Set cache control headers to prevent caching of authenticated pages
            response = None
            
            if user.is_superuser:
                response = redirect('admin_dashboard')
            elif Franchisee.objects.filter(user=user).exists():
                response = redirect('franchisee_dashboard')
            elif Franchisor.objects.filter(user=user).exists():
                response = redirect('franchisor_dashboard')
            else:
                messages.error(request, "No role assigned to this user.")
                logout(request)
                return redirect('login')
            
            # ✅ Disable browser caching for authenticated pages
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            return response
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'accounts/login.html')


def logout_view(request):
    """Logs out the user."""
    logout(request)
    messages.info(request, "You have been logged out.")
    
    # ✅ Clear cache after logout
    response = redirect('login')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response


# =========================================================================
# 2. MAIN APP VIEWS
# =========================================================================

def home_view(request):
    """Landing page."""
    return render(request, 'accounts/home.html')

# ✅ NEW: About page view
def about_view(request):
    """About page showing project overview, team, and tech stack."""
    return render(request, 'accounts/about.html')

# ✅ NEW: Support page view
def support_view(request):
    """Support page with FAQs, contact info, and help resources."""
    return render(request, 'accounts/support.html')

# ✅ NEW: Privacy Policy page view
def privacy_view(request):
    """Privacy policy page with data protection information."""
    return render(request, 'accounts/privacy.html')

@login_required
def browse(request):
    """Enhanced browse with location filtering - ONLY APPROVED franchises."""
    q = request.GET.get('q', '').strip()
    location_filter = request.GET.get('location', '').strip()
    
    # ✅ ONLY SHOW APPROVED FRANCHISES
    qs = Franchise.objects.filter(is_active=True, status='approved').select_related('franchisor')
    
    if q:
        qs = qs.filter(
            Q(name__icontains=q) |
            Q(category__icontains=q) |
            Q(description__icontains=q) |
            Q(franchisor__company_name__icontains=q) |
            Q(franchisor__country__icontains=q) |
            Q(franchisor__location__icontains=q)  # ✅ Include location in search
        )
    
    # ✅ Location filtering
    if location_filter:
        qs = qs.filter(
            Q(franchisor__location__icontains=location_filter) |
            Q(franchisor__country__icontains=location_filter)
        )
    
    franchises = qs.order_by('-created_at')

    applied_franchise_ids = []
    if Franchisee.objects.filter(user=request.user).exists():
        fe = Franchisee.objects.get(user=request.user)
        applied_franchise_ids = list(
            FranchiseApplication.objects.filter(franchisee=fe).values_list('franchise_id', flat=True)
        )

    response = render(request, 'accounts/browse.html', {
        'franchises': franchises,
        'q': q,
        'location_filter': location_filter,
        'applied_franchise_ids': applied_franchise_ids,
    })
    
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response


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
            
            # ✅ Redirect back to appropriate dashboard based on role
            if user.is_superuser:
                return redirect('admin_dashboard')
            elif Franchisor.objects.filter(user=user).exists():
                return redirect('franchisor_dashboard')
            elif Franchisee.objects.filter(user=user).exists():
                return redirect('franchisee_dashboard')
            else:
                return redirect('profile')
    else:
        form = ProfileForm(instance=user)

    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def edit_profile_view(request):
    """Allows users to edit their profile information."""
    # Get or create profile
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Update user fields
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()
        
        # Update profile fields
        profile.phone_number = request.POST.get('phone_number', '')
        profile.location = request.POST.get('location', '')
        profile.bio = request.POST.get('bio', '')
        
        # ✅ Handle profile picture upload - Only update if new file is uploaded
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']
        
        profile.save()
        
        messages.success(request, "Profile updated successfully!")
        
        # ✅ Redirect to appropriate dashboard based on role
        if request.user.is_superuser:
            return redirect('admin_dashboard')
        elif Franchisor.objects.filter(user=request.user).exists():
            return redirect('franchisor_dashboard')
        elif Franchisee.objects.filter(user=request.user).exists():
            return redirect('franchisee_dashboard')
        else:
            return redirect('profile')
    
    return render(request, 'accounts/edit_profile.html', {'profile': profile})


# =========================================================================
# 4. FRANCHISOR DASHBOARD + ADD FRANCHISE
# =========================================================================

@login_required
def franchisor_dashboard(request):
    """
    Displays the franchisor dashboard - SHOWS ALL FRANCHISES WITH STATUS
    """
    try:
        franchisor = Franchisor.objects.get(user=request.user)
    except Franchisor.DoesNotExist:
        messages.error(request, "You are not registered as a franchisor.")
        return redirect('browse')

    # ✅ ALL FRANCHISES (for approval status section at top)
    franchises = franchisor.franchises.filter(is_active=True).order_by('-submitted_at')

    # ✅ ONLY APPROVED FRANCHISES (for "My Franchises" section at bottom)
    approved_franchises = franchisor.franchises.filter(
        is_active=True,
        status='approved'
    ).order_by('-created_at')

    # Get unread notifications count
    unread_count = Notification.objects.filter(user=request.user, is_read=False).count()

    applications = []
    # Only get applications for APPROVED franchises
    for franchise in approved_franchises:
        applications += list(franchise.applications.all().order_by('-created_at'))

    applications = sorted(applications, key=lambda x: x.created_at, reverse=True)[:5]

    response = render(request, 'accounts/franchisor_dashboard.html', {
        'franchises': franchises,  # All franchises for approval status section
        'approved_franchises': approved_franchises,  # ✅ Only approved for "My Franchises"
        'applications': applications,
        'unread_notifications': unread_count,
    })
    
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

@login_required
def add_franchise_view(request):
    """Allows franchisors to create new franchises - NOW PENDING BY DEFAULT"""
    try:
        franchisor = Franchisor.objects.get(user=request.user)
    except Franchisor.DoesNotExist:
        messages.error(request, "You are not registered as a franchisor.")
        return redirect('browse')

    if request.method == 'POST':
        form = FranchiseForm(request.POST, request.FILES)
        location = request.POST.get('location', '').strip()
        
        # Debug: Log file upload attempt
        import logging
        logger = logging.getLogger(__name__)
        if 'image' in request.FILES:
            logger.info(f"📸 Image upload detected: {request.FILES['image'].name}")
            logger.info(f"📦 File size: {request.FILES['image'].size} bytes")
        
        if form.is_valid():
            franchise = form.save(commit=False)
            franchise.franchisor = franchisor
            franchise.status = 'pending'
            franchise.save()
            
            # Debug: Log saved image details
            if franchise.image:
                logger.info(f"✅ Franchise saved: {franchise.name}")
                logger.info(f"🔗 Image URL: {franchise.image.url}")
                logger.info(f"📁 Image name: {franchise.image.name}")
                logger.info(f"🏪 Storage backend: {franchise.image.storage.__class__.__name__}")
                logger.info(f"☁️ Storage location: {franchise.image.storage.__class__.__module__}")
            
            # ✅ Update franchisor location
            if location and location != franchisor.location:
                franchisor.location = location
                franchisor.save(update_fields=['location'])
            
            messages.success(request, f"Franchise '{franchise.name}' submitted successfully! It is now awaiting admin approval.")
            return redirect('franchisor_dashboard')
        else:
            logger.error(f"❌ Form validation failed: {form.errors}")
            messages.error(request, "Please correct the errors below.")
    else:
        form = FranchiseForm()

    return render(request, 'accounts/add_franchise.html', {'form': form})


@login_required
def delete_franchise(request, franchise_id):
    franchisor = Franchisor.objects.filter(user=request.user).first()
    if not franchisor:
        messages.error(request, "You are not registered as a franchisor.")
        return redirect('browse')

    franchise = get_object_or_404(Franchise, id=franchise_id, franchisor=franchisor)
    
    # ✅ Soft delete - keep in database but mark as inactive
    franchise.is_active = False
    franchise.save()
    
    # ✅ Create notification for admin users about the deletion
    admin_users = User.objects.filter(is_superuser=True)
    for admin in admin_users:
        Notification.objects.create(
            user=admin,
            title='Franchise Deleted by Franchisor',
            message=f'Franchisor "{franchisor.company_name}" deleted franchise "{franchise.name}"',
            notification_type='general',
            related_franchise=franchise
        )

    messages.success(request, f"Franchise '{franchise.name}' removed successfully.")
    return redirect('franchisor_dashboard')


@login_required
def edit_franchise_view(request, franchise_id):
    """Allows a franchisor to edit an existing franchise including documents"""
    try:
        franchisor = Franchisor.objects.get(user=request.user)
    except Franchisor.DoesNotExist:
        messages.error(request, "You are not registered as a franchisor.")
        return redirect('browse')

    franchise = get_object_or_404(Franchise, id=franchise_id, franchisor=franchisor, is_active=True)

    if request.method == 'POST':
        form = FranchiseForm(request.POST, request.FILES, instance=franchise)
        if form.is_valid():
            # ✅ Save the form - files will be handled automatically by Django/Cloudinary
            # Only update file fields if new files are provided in request.FILES
            updated_franchise = form.save(commit=False)
            
            # ✅ File fields are already handled by the form, no need to manually assign
            # Django forms automatically handle file uploads when request.FILES is passed
            
            updated_franchise.save()
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
        form = FranchiseApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.franchise = franchise
            app.franchisee = franchisee
            app.save()
            
            messages.success(request, f"Application submitted successfully for {franchise.name}!")
            return redirect('franchisee_dashboard')
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
    
    # 3. Active Franchises (ONLY ACTIVE ONES)
    active_franchises = Franchise.objects.filter(is_active=True).order_by('-created_at')[:5]
    
    # ✅ 4. Deleted/Soft-deleted Franchises (NEW)
    deleted_franchises = Franchise.objects.filter(is_active=False).order_by('-updated_at')[:10]

    # --- PART 2: ANALYTICS CHART DATA ---

    # CHART 1: New Users Per Month (Bar Chart)
    users_by_month = User.objects.annotate(month=TruncMonth('date_joined')).values('month').annotate(count=Count('id')).order_by('month')
    user_chart_labels = [item['month'].strftime('%b') for item in users_by_month] # e.g. ['Jan', 'Feb']
    user_chart_data = [item['count'] for item in users_by_month]

    # CHART 2: Applications Activity (Line Chart) - Replacing "Website Traffic"
    apps_by_month = FranchiseApplication.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month')
    traffic_chart_labels = [item['month'].strftime('%b') for item in apps_by_month]
    traffic_chart_data = [item['count'] for item in apps_by_month]

    # CHART 3: Top Franchises by Popularity (Applications count) - Replacing "Sales"
    popular_franchises = Franchise.objects.filter(is_active=True).annotate(app_count=Count('applications')).order_by('-app_count')[:5]
    sales_chart_labels = [f.name for f in popular_franchises]
    sales_chart_data = [f.app_count for f in popular_franchises]

    context = {
        # Lists
        'recent_approvals': recent_approvals,
        'recent_users': recent_users,
        'active_franchises': active_franchises,
        'deleted_franchises': deleted_franchises,  # ✅ NEW: Soft-deleted franchises
        
        # Charts
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

    response = render(request, 'accounts/franchisee_dashboard.html', {
        'applications': applications
    })
    
    # ✅ Prevent caching of dashboard
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

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

# =========================================================================
# 9. FORGOT PASSWORD VIEWS
# =========================================================================

def forgot_password_view(request):
    """Step 1: Enter username to initiate password reset."""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        
        if not username:
            messages.error(request, "Please enter your username.")
            return redirect('forgot_password')

        try:
            user = User.objects.get(username=username)
            # Store username in session for next step
            request.session['reset_username'] = username
            request.session['reset_step'] = 'questions'
            return redirect('forgot_password_questions')
        except User.DoesNotExist:
            # Don't reveal if username exists (security)
            messages.error(request, "If this username exists, you can proceed to security questions.")
            return redirect('forgot_password')

    return render(request, 'accounts/forgot_password.html')


def forgot_password_questions_view(request):
    """Step 2: Answer security questions."""
    username = request.session.get('reset_username')
    if not username or request.session.get('reset_step') != 'questions':
        messages.error(request, "Invalid password reset session.")
        return redirect('forgot_password')

    try:
        user = User.objects.get(username=username)
        sec_q = SecurityQuestion.objects.get(user=user)
        
        # Check if locked
        if sec_q.is_locked():
            messages.error(request, "Too many failed attempts. Please try again later.")
            return redirect('login')

        if request.method == 'POST':
            answer1 = request.POST.get('answer_1', '').strip()
            answer2 = request.POST.get('answer_2', '').strip()
            answer3 = request.POST.get('answer_3', '').strip()

            if sec_q.check_all_answers(answer1, answer2, answer3):
                # Success! Reset failed attempts and proceed
                sec_q.reset_failed_attempts()
                request.session['reset_step'] = 'newpassword'
                messages.success(request, "Security questions verified! Set your new password.")
                return redirect('forgot_password_reset')
            else:
                # Failed attempt
                sec_q.record_failed_attempt()
                remaining = 5 - sec_q.failed_attempts
                if remaining > 0:
                    messages.error(request, f"Incorrect answers. {remaining} attempts remaining.")
                else:
                    messages.error(request, "Account locked due to too many failed attempts. Try again in 1 hour.")
                    return redirect('login')

        return render(request, 'accounts/forgot_password_questions.html', {
            'question_1': sec_q.question_1,
            'question_2': sec_q.question_2,
            'question_3': sec_q.question_3,
        })

    except (User.DoesNotExist, SecurityQuestion.DoesNotExist):
        messages.error(request, "Security questions not set for this account.")
        return redirect('login')


def forgot_password_reset_view(request):
    """Step 3: Set new password after verification."""
    username = request.session.get('reset_username')
    if not username or request.session.get('reset_step') != 'newpassword':
        messages.error(request, "Invalid password reset session.")
        return redirect('forgot_password')

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('forgot_password_reset')

        if len(new_password) < 8:
            messages.error(request, "Password must be at least 8 characters.")
            return redirect('forgot_password_reset')

        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()

            # Clear session
            request.session.pop('reset_username', None)
            request.session.pop('reset_step', None)

            messages.success(request, "Password reset successfully! You can now login.")
            return redirect('login')

        except User.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect('login')

    return render(request, 'accounts/forgot_password_reset.html')

# =========================================================================
# 10. NOTIFICATION VIEWS (NEW)
# =========================================================================

@login_required
def notifications_view(request):
    """View all notifications for the current user"""
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'accounts/notifications.html', {
        'notifications': notifications
    })

@login_required
def mark_notification_read(request, notification_id):
    """Mark a single notification as read"""
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    
    return redirect('notifications')

@login_required
def mark_all_notifications_read(request):
    """Mark all notifications as read"""
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    
    return redirect('notifications')

@login_required
def get_notifications_api(request):
    """API endpoint for notification dropdown"""
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:10]
    unread_count = notifications.filter(is_read=False).count()
    
    data = {
        'unread_count': unread_count,
        'notifications': [
            {
                'id': str(n.id),
                'title': n.title,
                'message': n.message,
                'type': n.notification_type,
                'is_read': n.is_read,
                'created_at': n.created_at.strftime('%b %d, %Y at %I:%M %p'),
                'time_ago': get_time_ago(n.created_at),
            }
            for n in notifications
        ]
    }
    
    return JsonResponse(data)

def get_time_ago(dt):
    """Helper to get human-readable time difference"""
    from django.utils import timezone
    from datetime import timedelta
    
    now = timezone.now()
    diff = now - dt
    
    if diff < timedelta(minutes=1):
        return 'Just now'
    elif diff < timedelta(hours=1):
        mins = int(diff.total_seconds() / 60)
        return f'{mins} min ago' if mins == 1 else f'{mins} mins ago'
    elif diff < timedelta(days=1):
        hours = int(diff.total_seconds() / 3600)
        return f'{hours} hour ago' if hours == 1 else f'{hours} hours ago'
    elif diff < timedelta(days=7):
        days = diff.days
        return f'{days} day ago' if days == 1 else f'{days} days ago'
    else:
        return dt.strftime('%b %d, %Y')

# =========================================================================
# 11. CUSTOM ADMIN DASHBOARD VIEWS (NEW)
# =========================================================================

@login_required
@user_passes_test(is_admin, login_url='home')
def admin_franchise_management(request):
    """Custom Admin Dashboard - Franchise Management"""
    # Get franchise counts (ONLY ACTIVE)
    pending_count = Franchise.objects.filter(status='pending', is_active=True).count()
    approved_count = Franchise.objects.filter(status='approved', is_active=True).count()
    rejected_count = Franchise.objects.filter(status='rejected', is_active=True).count()
    
    # ✅ NEW: Count deleted franchises
    deleted_count = Franchise.objects.filter(is_active=False).count()
    
    # Get franchises by status (ONLY ACTIVE)
    pending_franchises = Franchise.objects.filter(
        status='pending', 
        is_active=True
    ).select_related('franchisor', 'franchisor__user').order_by('-submitted_at')
    
    approved_franchises = Franchise.objects.filter(
        status='approved', 
        is_active=True
    ).select_related('franchisor', 'franchisor__user').order_by('-reviewed_at')[:10]
    
    rejected_franchises = Franchise.objects.filter(
        status='rejected', 
        is_active=True
    ).select_related('franchisor', 'franchisor__user').order_by('-reviewed_at')[:10]
    
    # ✅ NEW: Get deleted franchises
    deleted_franchises = Franchise.objects.filter(
        is_active=False
    ).select_related('franchisor', 'franchisor__user').order_by('-updated_at')[:20]
    
    return render(request, 'accounts/admin_franchise_management.html', {
        'pending_count': pending_count,
        'approved_count': approved_count,
        'rejected_count': rejected_count,
        'deleted_count': deleted_count,  # ✅ NEW
        'pending_franchises': pending_franchises,
        'approved_franchises': approved_franchises,
        'rejected_franchises': rejected_franchises,
        'deleted_franchises': deleted_franchises,  # ✅ NEW
    })

@login_required
@user_passes_test(is_admin, login_url='home')
def admin_franchise_detail(request, franchise_id):
    """View detailed information about a franchise for admin review"""
    franchise = get_object_or_404(Franchise, id=franchise_id)
    
    return render(request, 'accounts/admin_franchise_detail.html', {
        'franchise': franchise
    })

@require_POST
@login_required
@user_passes_test(is_admin, login_url='home')
def admin_approve_franchise(request, franchise_id):
    """Admin approves a pending franchise"""
    franchise = get_object_or_404(Franchise, id=franchise_id, status='pending')
    
    franchise.approve(request.user)
    
    messages.success(request, f"Franchise '{franchise.name}' has been approved!")
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'message': 'Franchise approved'})
    
    return redirect('admin_franchise_management')

@require_POST
@login_required
@user_passes_test(is_admin, login_url='home')
def admin_reject_franchise(request, franchise_id):
    """Admin rejects a pending franchise"""
    franchise = get_object_or_404(Franchise, id=franchise_id, status='pending')
    
    reason = request.POST.get('rejection_reason', '').strip()
    if not reason:
        messages.error(request, "Rejection reason is required.")
        return redirect('admin_franchise_detail', franchise_id=franchise_id)
    
    franchise.reject(request.user, reason)
    
    messages.success(request, f"Franchise '{franchise.name}' has been rejected.")
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'message': 'Franchise rejected'})
    
    return redirect('admin_franchise_management')

# ✅ NEW: Permanent Delete Functions for Admin
@require_http_methods(["DELETE", "POST"])  # Allow both DELETE and POST
@login_required
@user_passes_test(is_admin, login_url='home')
def admin_permanent_delete_franchise(request, franchise_id):
    """Permanently delete a soft-deleted franchise from database"""
    try:
        # Only allow deleting soft-deleted franchises
        franchise = get_object_or_404(Franchise, id=franchise_id, is_active=False)
        
        franchise_name = franchise.name
        
        # Permanently delete from database
        franchise.delete()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'message': f'Franchise "{franchise_name}" permanently deleted'
            })
        
        messages.success(request, f'Franchise "{franchise_name}" permanently deleted.')
        return redirect('admin_dashboard')
        
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
        
        messages.error(request, f'Error deleting franchise: {str(e)}')
        return redirect('admin_dashboard')


@require_http_methods(["DELETE", "POST"])  # Allow both DELETE and POST
@login_required
@user_passes_test(is_admin, login_url='home')
def admin_permanent_delete_all_franchises(request):
    """Permanently delete ALL soft-deleted franchises from database"""
    try:
        # Get all soft-deleted franchises
        deleted_franchises = Franchise.objects.filter(is_active=False)
        count = deleted_franchises.count()
        
        if count == 0:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'message': 'No deleted franchises found'
                }, status=404)
            
            messages.warning(request, 'No deleted franchises to remove.')
            return redirect('admin_dashboard')
        
        # Permanently delete all
        deleted_franchises.delete()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'message': f'{count} franchise(s) permanently deleted',
                'count': count
            })
        
        messages.success(request, f'{count} franchise(s) permanently deleted.')
        return redirect('admin_dashboard')
        
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
        
        messages.error(request, f'Error deleting franchises: {str(e)}')
        return redirect('admin_dashboard')

# =========================================================================
# 12. FAVORITES/WATCHLIST VIEWS (NEW)
# =========================================================================

@login_required
def favorites_view(request):
    """
    Display user's favorited franchises in a modern, responsive grid layout
    """
    # Get all favorites for current user
    favorites = UserFavorites.objects.filter(
        user=request.user
    ).select_related('franchise', 'franchise__franchisor').order_by('-created_at')
    
    # Get only active and approved franchises
    active_favorites = [
        fav for fav in favorites 
        if fav.franchise.is_active and fav.franchise.status == 'approved'
    ]
    
    context = {
        'favorites': active_favorites,
        'total_count': len(active_favorites)
    }
    
    return render(request, 'accounts/favorites.html', context)


@require_http_methods(["POST"])
@login_required
def toggle_favorite(request, franchise_id):
    """
    AJAX endpoint to add or remove a franchise from favorites
    Returns JSON response for dynamic UI updates
    """
    try:
        franchise = get_object_or_404(
            Franchise, 
            id=franchise_id, 
            is_active=True, 
            status='approved'
        )
        
        # Check if already favorited
        favorite = UserFavorites.objects.filter(
            user=request.user,
            franchise=franchise
        ).first()
        
        if favorite:
            # Remove from favorites
            favorite.delete()
            return JsonResponse({
                'status': 'removed',
                'message': f'{franchise.name} removed from favorites',
                'is_favorited': False
            })
        else:
            # Add to favorites
            UserFavorites.objects.create(
                user=request.user,
                franchise=franchise
            )
            return JsonResponse({
                'status': 'added',
                'message': f'{franchise.name} added to favorites',
                'is_favorited': True
            })
            
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


@login_required
def check_favorite(request, franchise_id):
    """
    Check if a franchise is favorited by the current user
    Used for initial page load state
    """
    is_favorited = UserFavorites.objects.filter(
        user=request.user,
        franchise_id=franchise_id
    ).exists()
    
    return JsonResponse({
        'is_favorited': is_favorited
    })

@login_required
def application_detail_view(request, application_id):
    """
    Display detailed information about a specific franchise application.
    Only accessible by the franchisor who owns the franchise.
    """
    application = get_object_or_404(FranchiseApplication, id=application_id)
    
    # Security check: Only the franchisor who owns the franchise can view this
    try:
        franchisor = Franchisor.objects.get(user=request.user)
        if application.franchise.franchisor != franchisor:
            messages.error(request, "You don't have permission to view this application.")
            return redirect('franchisor_dashboard')
    except Franchisor.DoesNotExist:
        messages.error(request, "You are not registered as a franchisor.")
        return redirect('home')
    
    return render(request, 'accounts/application_detail.html', {
        'application': application
    })

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
def dashboard_stats(request):
    """Return real-time dashboard statistics as JSON"""
    if not request.user.is_authenticated or not hasattr(request.user, 'franchisor'):
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    franchisor = request.user.franchisor
    
    # Get franchise counts
    approved_franchises = franchisor.franchises.filter(status='approved').count()
    total_applications = franchisor.franchises.values_list('applications', flat=True).count()
    
    # Calculate active franchisees (unique applicants)
    from django.db.models import Count
    active_franchisees = franchisor.franchises.aggregate(
        franchisees=Count('applications__franchisee', distinct=True)
    )['franchisees'] or 0
    
    # Calculate revenue (approximation: approved franchises × base fee)
    revenue = approved_franchises * 50000
    
    return JsonResponse({
        'active_franchises': approved_franchises,
        'total_applications': total_applications,
        'active_franchisees': active_franchisees,
        'revenue': revenue
    })

# =========================================================================
# 13. CUSTOM SYSTEM ADMIN VIEWS
# =========================================================================

def is_superuser(user):
    return user.is_authenticated and user.is_superuser

@login_required
@user_passes_test(is_superuser, login_url='login')
def admin_index(request):
    """Renders the main admin dashboard home."""
    return render(request, 'accounts/mainadmin.html')

@login_required
@user_passes_test(is_superuser, login_url='login')
def admin_user_list(request):
    """Lists users with filtering logic matching your HTML."""
    users = User.objects.all().order_by('-date_joined')
    
    # --- Filter Logic ---
    staff_filter = request.GET.get('staff')
    superuser_filter = request.GET.get('superuser')
    active_filter = request.GET.get('active')

    filters = {
        'staff': staff_filter,
        'superuser': superuser_filter,
        'active': active_filter
    }

    if staff_filter == 'yes':
        users = users.filter(is_staff=True)
    elif staff_filter == 'no':
        users = users.filter(is_staff=False)

    if superuser_filter == 'yes':
        users = users.filter(is_superuser=True)
    elif superuser_filter == 'no':
        users = users.filter(is_superuser=False)

    if active_filter == 'yes':
        users = users.filter(is_active=True)
    elif active_filter == 'no':
        users = users.filter(is_active=False)

    context = {
        'users': users,
        'count': users.count(),
        'filters': filters
    }
    return render(request, 'accounts/userlist.html', context)

@login_required
@user_passes_test(is_superuser, login_url='login')
def admin_add_user(request):
    """Handles adding a new user."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
        else:
            try:
                # Create the user
                user = User.objects.create_user(username=username, password=password)
                messages.success(request, f"User {username} created successfully.")
                
                # Button Logic
                if 'save_add_another' in request.POST:
                    return redirect('admin_add_user')
                elif 'save_continue' in request.POST:
                    return redirect('admin_change_user', user_id=user.id)
                else:
                    return redirect('admin_user_list')
            except Exception as e:
                messages.error(request, f"Error creating user: {e}")

    return render(request, 'accounts/adduser.html')

@login_required
@user_passes_test(is_superuser, login_url='login')
def admin_change_user(request, user_id):
    """Handles editing user details and permissions."""
    target_user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        # 1. Update Basic Info
        target_user.username = request.POST.get('username')
        target_user.first_name = request.POST.get('first_name', '')
        target_user.last_name = request.POST.get('last_name', '')
        target_user.email = request.POST.get('email', '')

        # 2. Update Permissions (Checkboxes return 'on' if checked, None if not)
        target_user.is_active = request.POST.get('is_active') == 'on'
        target_user.is_staff = request.POST.get('is_staff') == 'on'
        target_user.is_superuser = request.POST.get('is_superuser') == 'on'

        try:
            target_user.save()
            messages.success(request, f"User {target_user.username} updated successfully.")

            if 'save_add_another' in request.POST:
                return redirect('admin_add_user')
            elif 'save_continue' in request.POST:
                return redirect('admin_change_user', user_id=target_user.id)
            else:
                return redirect('admin_user_list')
                
        except Exception as e:
            messages.error(request, f"Error updating user: {e}")

    return render(request, 'accounts/changeuser.html', {'target_user': target_user})

@login_required
@user_passes_test(is_superuser, login_url='login')
def admin_delete_user(request, user_id):
    """Deletes a user."""
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        if user == request.user:
            messages.error(request, "You cannot delete yourself.")
        else:
            user.delete()
            messages.success(request, "User deleted successfully.")
    return redirect('admin_user_list')

@login_required
@user_passes_test(is_superuser, login_url='login')
def admin_password_change(request):
    """Allows the admin to change their OWN password."""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Important: Keeps the user logged in after password change
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated!")
            return redirect('admin_password_change')
        else:
            messages.error(request, "Please correct the errors below.")
    return render(request, 'accounts/passwordchange.html')