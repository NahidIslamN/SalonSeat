from rest_framework import serializers
from jayla_models.models import Listing, Photo_Media
from auths.models import CustomUser


class PhotoMediaPublicSerializer(serializers.ModelSerializer):
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


class CreatorSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "full_name", "phone", "image", "user_role"]


class ListingPublicSerializer(serializers.ModelSerializer):
    photos = PhotoMediaPublicSerializer(many=True, read_only=True)
    creator = serializers.SerializerMethodField()

    class Meta:
        model = Listing
        fields = [
            "id",
            "creator",
            "businessname",
            "listing_title",
            "street_address",
            "city",
            "zip",
            "country",
            "map_link",
            "longitude",
            "latitude",
            "price",
            "availability_status",
            "rental_type",
            "maximum_cccupancy",
            "amenities_description",
            "is_wifi",
            "is_parking",
            "is_storage",
            "photos",
            "create_at",
        ]

    def get_creator(self, obj):
        user = getattr(obj, 'creator', None) or getattr(obj, 'crearor', None)
        if not user:
            return None
        return CreatorSummarySerializer(user, context=self.context).data
