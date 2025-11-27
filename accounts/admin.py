from django.contrib import admin
from .models import (
    Franchisee,
    Franchisor,
    AdminProfile,
    Franchise,
    FranchiseApplication,
    Notification,
    Profile,
    SecurityQuestion
)

# ✅ FRANCHISE APPLICATION ADMIN
@admin.register(FranchiseApplication)
class FranchiseApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'franchise', 'franchisee', 'email', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'franchise')
    search_fields = ('full_name', 'email', 'franchise__name', 'franchisee__business_name')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Application Info', {
            'fields': ('franchise', 'franchisee', 'status')
        }),
        ('Applicant Details', {
            'fields': ('full_name', 'email', 'phone', 'experience')
        }),
        ('Review Notes', {
            'fields': ('approval_note', 'rejection_reason'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_applications', 'reject_applications']
    
    def approve_applications(self, request, queryset):
        """Bulk approve selected applications"""
        updated = queryset.update(status='Approved')
        self.message_user(request, f'{updated} application(s) approved successfully.')
    approve_applications.short_description = "Approve selected applications"
    
    def reject_applications(self, request, queryset):
        """Bulk reject selected applications"""
        updated = queryset.update(status='Rejected')
        self.message_user(request, f'{updated} application(s) rejected.')
    reject_applications.short_description = "Reject selected applications"

# ✅ FRANCHISE ADMIN
@admin.register(Franchise)
class FranchiseAdmin(admin.ModelAdmin):
    list_display = ('name', 'franchisor', 'category', 'status', 'investment', 'submitted_at', 'is_active')
    list_filter = ('status', 'is_active', 'category', 'submitted_at')
    search_fields = ('name', 'category', 'description', 'franchisor__company_name')
    readonly_fields = ('id', 'submitted_at', 'reviewed_at', 'created_at', 'updated_at')
    list_per_page = 25
    date_hierarchy = 'submitted_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category', 'franchisor', 'investment', 'description', 'image')
        }),
        ('Status', {
            'fields': ('status', 'is_active')
        }),
        ('Review Information', {
            'fields': ('reviewed_by', 'reviewed_at', 'rejection_reason'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('id', 'submitted_at', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_franchises', 'reject_franchises', 'deactivate_franchises']
    
    def approve_franchises(self, request, queryset):
        """Bulk approve pending franchises"""
        updated = 0
        for franchise in queryset.filter(status='pending'):
            franchise.approve(request.user)
            updated += 1
        self.message_user(request, f'{updated} franchise(s) approved successfully.')
    approve_franchises.short_description = "Approve selected franchises"
    
    def reject_franchises(self, request, queryset):
        """Bulk reject pending franchises"""
        updated = 0
        for franchise in queryset.filter(status='pending'):
            franchise.reject(request.user, reason="Bulk rejection by admin")
            updated += 1
        self.message_user(request, f'{updated} franchise(s) rejected.')
    reject_franchises.short_description = "Reject selected franchises"
    
    def deactivate_franchises(self, request, queryset):
        """Soft delete franchises"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} franchise(s) deactivated.')
    deactivate_franchises.short_description = "Deactivate selected franchises"

# ✅ NOTIFICATION ADMIN
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('title', 'message', 'user__username')
    readonly_fields = ('id', 'created_at')
    list_per_page = 30
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Notification Details', {
            'fields': ('user', 'title', 'message', 'notification_type')
        }),
        ('Related Data', {
            'fields': ('related_franchise', 'is_read')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} notification(s) marked as read.')
    mark_as_read.short_description = "Mark as read"
    
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} notification(s) marked as unread.')
    mark_as_unread.short_description = "Mark as unread"

# ✅ FRANCHISEE ADMIN
@admin.register(Franchisee)
class FranchiseeAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'user', 'contact_number', 'joined_date')
    search_fields = ('business_name', 'user__username', 'user__email')
    readonly_fields = ('id', 'joined_date')
    list_per_page = 25

# ✅ FRANCHISOR ADMIN
@admin.register(Franchisor)
class FranchisorAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'email', 'phone', 'country', 'created_at')
    search_fields = ('company_name', 'user__username', 'email', 'country')
    readonly_fields = ('id', 'created_at')
    list_per_page = 25

# ✅ PROFILE ADMIN
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone_number', 'location')
    search_fields = ('user__username', 'full_name', 'phone_number')
    list_filter = ('location',)

# ✅ SECURITY QUESTION ADMIN
@admin.register(SecurityQuestion)
class SecurityQuestionAdmin(admin.ModelAdmin):
    list_display = ('user', 'failed_attempts', 'locked_until', 'created_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    list_filter = ('locked_until', 'created_at')

# ✅ ADMIN PROFILE ADMIN
@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'role_description', 'created_at')
    search_fields = ('full_name', 'user__username')
    readonly_fields = ('id', 'created_at')
