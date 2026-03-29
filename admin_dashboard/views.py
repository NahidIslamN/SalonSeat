from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *

from rest_framework.permissions import IsAdminUser
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from chats.tasks import sent_note_to_user
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from jayla_models.models import Listing, Photo_Media
from SalonSeat.pagination import CustomPagination
# Create your views here.



class ListingAdminViewFilters(APIView):
    permission_classes = [IsAdminUser]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request):
        search = request.GET.get('filter')
        if search == 'active':        
            listings = Listing.objects.filter(is_admin_approved=True, availability_status='active').order_by("-create_at")
        
        elif search == 'paused': 
          
            listings = Listing.objects.filter(is_admin_approved=True, availability_status='paused').order_by("-create_at")
        
        elif search == 'draft':            
            listings = Listing.objects.filter(is_admin_approved=True, availability_status='draft').order_by("-create_at")
        
        elif search == 'pending':            
            listings = Listing.objects.filter(is_admin_approved=False,is_admin_rejected=False).order_by("-create_at")
        
            

        else:
           
            listings = Listing.objects.filter().order_by("-create_at")

        paginator = CustomPagination()
        page = paginator.paginate_queryset(listings, request, view=self)
        serializer = ListingReadSerializerAdmin(page, many=True, context={"request": request})
        return paginator.get_paginated_response(serializer.data)
    

class ListingAdminView(APIView):
    permission_classes = [IsAdminUser]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    parser_classes = [MultiPartParser, FormParser, JSONParser]


    def _get_listing(self, request, pk):
        return Listing.objects.filter(pk=pk).first()


    
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
                "data": ListingReadSerializerAdmin(listing, context={"request": request}).data,
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

        serializer = ListingWriteSerializerAdmin(listing, data=request.data, partial=partial)
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
                "data": ListingReadSerializerAdmin(listing, context={"request": request}).data,
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




