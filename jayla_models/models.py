from django.db import models
from auths.models import CustomUser

# Create your models here.

class Photo_Media(models.Model):
    images = models.ImageField(upload_to='listings')

    def delete(self, using=None, keep_parents=False):
        if self.images:
            self.images.delete(save=False)
        return super().delete(using=using, keep_parents=keep_parents)


class Listing(models.Model):
    crearor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_admin_approved = models.BooleanField(default=False)
    is_admin_rejected = models.BooleanField(default=False)

    #Basic Information
    businessname = models.CharField(max_length=250)
    listing_title = models.CharField(max_length=250)
    street_address = models.TextField()
    city = models.CharField(max_length=250)
    zip = models.CharField(max_length=250)
    country = models.CharField(max_length=250)
    map_link = models.URLField(verbose_name="listing location") 


    #Amenities
    is_wifi = models.BooleanField(default=False)
    is_parking = models.BooleanField(default=False)
    is_storage = models.BooleanField(default=False)
    is_mirror = models.BooleanField(default=False)
    is_sink = models.BooleanField(default=False)
    is_styling_chair = models.BooleanField(default=False)
    is_product_shelves = models.BooleanField(default=False)
    is_access_24_hours = models.BooleanField(default=False)
    amenities_description = models.TextField()

    # Rental Details
    STATUS = (
        ('active','Active'),
        ('paused', 'Paused'),
        ('draft',"Draft")
    )

    rental_type = models.CharField(max_length=250)
    lease_terms = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    availability_status = models.CharField(max_length=250, choices=STATUS, default='paused')
    maximum_cccupancy = models.IntegerField()

    # Photos & Media
    photos = models.ManyToManyField(Photo_Media, related_name='photos_and_media')

    restrictions = models.TextField()
    additional_notes = models.TextField()

    is_deleted = models.BooleanField(default=False)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ID:{self.id} - {self.businessname} - {self.listing_title}"

    def delete(self, using=None, keep_parents=False):
        for photo in self.photos.all():
            is_used_elsewhere = photo.photos_and_media.exclude(pk=self.pk).exists()
            if not is_used_elsewhere:
                photo.delete()
        return super().delete(using=using, keep_parents=keep_parents)
