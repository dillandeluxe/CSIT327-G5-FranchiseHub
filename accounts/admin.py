from django.contrib import admin
from .models import FranchiseApplication

@admin.register(FranchiseApplication)
class FranchiseApplicationAdmin(admin.ModelAdmin):
    list_display = ('franchise', 'franchisee', 'full_name', 'email', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'franchise')
    search_fields = ('full_name', 'email', 'franchise__name', 'franchisee__business_name')
    readonly_fields = ('created_at',)
    fields = (
        'franchise', 'franchisee',
        'full_name', 'email', 'phone', 'experience',
        'status', 'approval_note', 'rejection_reason',
        'created_at',
    )
