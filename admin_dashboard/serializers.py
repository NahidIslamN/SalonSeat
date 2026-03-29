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
