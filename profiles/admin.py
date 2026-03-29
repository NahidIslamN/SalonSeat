from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    # Columns to display in the admin list view
    list_display = (
        'user', 'business_name', 'company', 'job_title', 
        'city', 'country', 'gender', 'created_at'
    )
    
    # Filters on the right sidebar
    list_filter = (
        'gender', 'city', 'country', 'company', 'job_title', 'created_at'
    )
    
    # Search box fields
    search_fields = (
        'user__email', 'business_name', 'company', 'job_title', 'city', 'country'
    )
    
    # Optional: ordering in admin list view
    ordering = ('-created_at',)
    
    # Optional: make fields readonly
    readonly_fields = ('created_at', 'updated_at')
    
    # Optional: date hierarchy for easy navigation by date
    date_hierarchy = 'created_at'

    # Optional: fieldsets to organize detail view in admin
    fieldsets = (
        ('User Info', {
            'fields': ('user', 'business_name', 'bio', 'website')
        }),
        ('Location Info', {
            'fields': ('address', 'city', 'country', 'postal_code')
        }),
        ('Professional Info', {
            'fields': ('company', 'job_title')
        }),
        ('Social Links', {
            'fields': ('facebook', 'linkedin', 'twitter')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )