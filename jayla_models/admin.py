from django.contrib import admin
from .models import Listing, Photo_Media

# Register your models here.




class PhotoMediaInline(admin.TabularInline):
    model = Listing.photos.through
    extra = 1


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'businessname',
        'listing_title',
        'city',
        'country',
        'price',
        'availability_status',
        'is_admin_approved'
    )

    search_fields = (
        'businessname',
        'listing_title',
        'city',
        'country',
        'street_address',
        'zip'
    )

    list_filter = (
        'availability_status',
        'is_admin_approved',
        'city',
        'country',
        'is_wifi',
        'is_parking',
        'is_storage',
        'is_mirror',
        'is_sink',
        'is_styling_chair',
        'is_product_shelves',
        'is_access_24_hours'
    )

    list_editable = (
        'availability_status',
        'is_admin_approved'
    )

    inlines = [PhotoMediaInline]


@admin.register(Photo_Media)
class PhotoMediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'images')