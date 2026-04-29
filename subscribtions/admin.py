from django.contrib import admin
from .models import Feature, SubscriptionPlan


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('id', 'text')
    search_fields = ('text',)


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'price',
        'listing_limit',
        'media_limit',
        'is_unlimited_listing',
        'is_able_analytics',
    )

    # Search functionality
    search_fields = ('id', 'price')

    # Filters (right sidebar)
    list_filter = (
        'is_unlimited_listing',
        'is_able_analytics',
        'features',
    )

    # Better UI for ManyToMany
    filter_horizontal = ('features',)

    # Optional: ordering
    ordering = ('-id',)

    # Optional: pagination
    list_per_page = 20