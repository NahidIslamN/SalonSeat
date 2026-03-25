from rest_framework import serializers

from jayla_models.models import Listing, Photo_Media


class PhotoMediaReadSerializer(serializers.ModelSerializer):
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


class ListingReadSerializer(serializers.ModelSerializer):
	photos = PhotoMediaReadSerializer(many=True, read_only=True)

	class Meta:
		model = Listing
		fields = [
			"id",
			"is_admin_approved",
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


class ListingWriteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Listing
		fields = [
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
