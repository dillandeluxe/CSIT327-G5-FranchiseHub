# This is accounts/admin.py

from django.contrib import admin
from .models import FranchiseApplication, Franchise, Franchisee, Franchisor, Profile, AdminProfile
from django_admin_charts.admin import AdminChartMixin
from django_admin_charts.charts import Chart

# ===============================================
# This is the important part for your chart!
# ===============================================

@admin.register(FranchiseApplication)
class FranchiseApplicationAdmin(AdminChartMixin, admin.ModelAdmin):
    """
    This is the admin configuration for your FranchiseApplication model.
    """
    # 1. We add the `AdminChartMixin` to enable charts
    
    list_display = ('full_name', 'franchise', 'status', 'created_at')
    list_filter = ('status', 'franchise')
    search_fields = ('full_name', 'email')

    # 2. This method defines all the charts for this model
    def get_admin_charts(self):
        
        # Chart 1: Application Status Pie Chart
        pie_chart = Chart(
            # The name of the chart
            title='Application Status (Pie Chart)',
            
            # The type of chart (e.g., 'bar', 'line', 'pie', 'doughnut')
            chart_type='pie',
            
            # The model we are querying
            model=FranchiseApplication,
            
            # The field we are grouping by
            # This uses your `status` field with its 'Pending', 'Approved' choices
            fields=['status'],
        )
        
        # Chart 2: Applications per Day (Line Chart)
        line_chart = Chart(
            title='New Applications per Day (Line Chart)',
            chart_type='line',
            model=FranchiseApplication,
            
            # This tells the chart to use the 'created_at' field
            # and group the counts by 'day'
            time_series=True,
            time_series_options={
                'field': 'created_at',
                'interval': 'day',
            },
        )

        # 3. Return a list of all the charts you want to display
        return [pie_chart, line_chart]

# ===============================================
# Register your other models so you can see them
# in the admin area (without charts, for now)
# ===============================================

@admin.register(Franchise)
class FranchiseAdmin(admin.ModelAdmin):
    list_display = ('name', 'franchisor', 'category', 'investment', 'is_active')
    list_filter = ('category', 'is_active', 'franchisor')
    search_fields = ('name', 'description')

@admin.register(Franchisee)
class FranchiseeAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'user', 'contact_number', 'joined_date')
    search_fields = ('business_name', 'user__username')

@admin.register(Franchisor)
class FranchisorAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'email', 'country', 'created_at')
    search_fields = ('company_name', 'user__username')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone_number', 'location')
    search_fields = ('full_name', 'user__username')

@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'role_description')
    search_fields = ('full_name', 'user__username')