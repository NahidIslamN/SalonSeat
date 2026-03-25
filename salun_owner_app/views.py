from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from SalonSeat.custom_permission import IsProfissional, IsSalunOwner
from rest_framework.permissions import IsAdminUser
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from chats.tasks import sent_note_to_user
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from jayla_models.models import Listing, Photo_Media
from SalonSeat.pagination import CustomPagination

# Create your views here.


class SalunListingView(APIView):
    permission_classes = [IsSalunOwner]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request):
        listings = Listing.objects.filter(crearor=request.user).order_by("-create_at")
        paginator = CustomPagination()
        page = paginator.paginate_queryset(listings, request, view=self)
        serializer = ListingReadSerializer(page, many=True, context={"request": request})
        return paginator.get_paginated_response(serializer.data)
    

    def post(self, request):
        serializer = ListingWriteSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        listing = serializer.save(crearor=request.user)

        images = request.FILES.getlist("images")
        for image in images:
            photo = Photo_Media.objects.create(images=image)
            listing.photos.add(photo)

        return Response(
            {
                "success": True,
                "message": "Listing created successfully.",
                "data": ListingReadSerializer(listing, context={"request": request}).data,
            },
            status=status.HTTP_201_CREATED,
        )


class SalunListingDetailView(APIView):
    permission_classes = [IsSalunOwner]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def _get_listing(self, request, pk):
        return Listing.objects.filter(pk=pk, crearor=request.user).first()

    def get(self, request, pk):
        listing = self._get_listing(request, pk)
        if listing is None:
            return Response(
                {"success": False, "message": "Listing not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(
            {
                "success": True,
                "data": ListingReadSerializer(listing, context={"request": request}).data,
            },
            status=status.HTTP_200_OK,
        )

    def put(self, request, pk):
        return self._update(request, pk, partial=False)

    def patch(self, request, pk):
        return self._update(request, pk, partial=True)

    def _update(self, request, pk, partial):
        listing = self._get_listing(request, pk)
        if listing is None:
            return Response(
                {"success": False, "message": "Listing not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = ListingWriteSerializer(listing, data=request.data, partial=partial)
        if not serializer.is_valid():
            return Response(
                {"success": False, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        listing = serializer.save()

        replace_images_raw = request.data.get("replace_images", "false")
        replace_images = str(replace_images_raw).lower() in {"1", "true", "yes"}

        if replace_images:
            for photo in listing.photos.all():
                is_used_elsewhere = photo.photos_and_media.exclude(pk=listing.pk).exists()
                if not is_used_elsewhere:
                    photo.delete()
            listing.photos.clear()

        images = request.FILES.getlist("images")
        for image in images:
            photo = Photo_Media.objects.create(images=image)
            listing.photos.add(photo)

        return Response(
            {
                "success": True,
                "message": "Listing updated successfully.",
                "data": ListingReadSerializer(listing, context={"request": request}).data,
            },
            status=status.HTTP_200_OK,
        )

    def delete(self, request, pk):
        listing = self._get_listing(request, pk)
        if listing is None:
            return Response(
                {"success": False, "message": "Listing not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        for photo in listing.photos.all():
            is_used_elsewhere = photo.photos_and_media.exclude(pk=listing.pk).exists()
            if not is_used_elsewhere:
                photo.delete()
        listing.photos.clear()
        listing.delete()

        return Response(
            {"success": True, "message": "Listing deleted permanently."},
            status=status.HTTP_200_OK,
        )


class SalunListingMediaDeleteView(APIView):
    permission_classes = [IsSalunOwner]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def delete(self, request, pk):
        photo = Photo_Media.objects.filter(pk=pk).first()
        if photo is None:
            return Response(
                {"success": False, "message": "Media not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        linked_listings = photo.photos_and_media.all()
        if not linked_listings.exists():
           
            return Response(
                {
                    "success": False,
                    "message": "Media is not linked to any listing.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        used_by_other_owner = linked_listings.exclude(crearor=request.user).exists()
        if used_by_other_owner:
            return Response(
                {
                    "success": False,
                    "message": "You can't delete media used by another owner's listing.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        photo.delete()  # deletes file permanently via model delete()

        return Response(
            {"success": True, "message": "Media deleted permanently."},
            status=status.HTTP_200_OK,
        )
  