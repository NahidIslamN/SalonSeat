from rest_framework import serializers
from jayla_models.models import Listing, Photo_Media
from auths.models import CustomUser


class PhotoMediaReadSerializerAdmin(serializers.ModelSerializer):
	url = serializers.SerializerMethodField()
	
	class Meta:
		model = Photo_Media
		fields = ["id", "url"]
		
	def get_url(self, obj):
		if not obj.images:
			return None
		request = self.context.get("request")
		if request is None:
			return obj.images.url
		return request.build_absolute_uri(obj.images.url)


class CustomUserSerializerAdmin(serializers.ModelSerializer):
	class Meta:
		model = CustomUser
		fields = [
            "email",
            "full_name",
            "phone",
            "user_role",
            "image",
            "latitude",
            "longitude",
        ]


class ListingReadSerializerAdmin(serializers.ModelSerializer):
	photos = PhotoMediaReadSerializerAdmin(many=True, read_only=True)
	crearor = CustomUserSerializerAdmin(read_only=True)
	class Meta:
		model = Listing
		fields = [
			"id",
			"crearor",
			"is_admin_approved",
			"is_admin_rejected",
			"businessname",
			"listing_title",
			"street_address",
			"city",
			"zip",
			"country",
			"map_link",
			"is_wifi",
			"is_parking",
			"is_storage",
			"is_mirror",
			"is_sink",
			"is_styling_chair",
			"is_product_shelves",
			"is_access_24_hours",
			"amenities_description",
			"rental_type",
			"lease_terms",
			"price",
			"availability_status",
			"maximum_cccupancy",
			"restrictions",
			"additional_notes",
			"photos",
			"create_at",
			"update_at",
		]
		

class ListingWriteSerializerAdmin(serializers.ModelSerializer):
	class Meta:
		model = Listing
		fields = [
			"is_admin_approved",
			"is_admin_rejected",
			"businessname",
			"listing_title",
			"street_address",
			"city",
			"zip",
			"country",
			"map_link",
			"is_wifi",
			"is_parking",
			"is_storage",
			"is_mirror",
			"is_sink",
			"is_styling_chair",
			"is_product_shelves",
			"is_access_24_hours",
			"amenities_description",
			"rental_type",
			"lease_terms",
			"price",
			"availability_status",
			"maximum_cccupancy",
			"restrictions",
			"additional_notes",
		]








################################### user management admin ######################################


from rest_framework import serializers
from auths.models import CustomUser
from profiles.models import UserProfile
import os
from django.core.files.base import ContentFile


class UserProfileSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'id',
            'business_name',
            'address',
            'date_of_birth',
            'gender',
            'city',
            'country',
            'postal_code',
            'bio',
            'website',
            'facebook',
            'linkedin',
            'twitter',
            'company',
            'job_title'
        ]


class CustomUserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializerAdmin(read_only=True)
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'email',
            'full_name',
            'phone',
            'user_role',
            'image',
            'is_active',
            'is_staff',
            'is_email_verified',
            'status',
            'created_at',
            'profile'
        ]
        read_only_fields = ['id', 'email', 'created_at']

    def update(self, instance, validated_data):
        image = validated_data.pop('image', None)

        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.status = validated_data.get('status', instance.status)

        if image:
            if instance.image:
                try:
                    instance.image.delete(save=False)
                except Exception:
                    pass

            original_name = image.name
            ext = os.path.splitext(original_name)[1]
            new_filename = f"profile/{instance.id}{ext}"
            instance.image.save(new_filename, image, save=False)

        instance.save()
        return instance



