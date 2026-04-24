from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from SalonSeat.custom_permission import IsProfissional
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from chats.tasks import sent_note_to_user
from jayla_models.models import Listing, Photo_Media
from SalonSeat.pagination import CustomPagination
from django.db import models


# Create your views here.


class ListingViewBeautyProfission(APIView):
    permission_classes = [IsProfissional]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get(self, request):
        qs = Listing.objects.filter(is_admin_approved=True, availability_status='active', is_deleted=False)

        # Text search
        q = request.GET.get('q')
        if q:
            qs = qs.filter(
                models.Q(businessname__icontains=q)
                | models.Q(listing_title__icontains=q)
                | models.Q(amenities_description__icontains=q)
                | models.Q(additional_notes__icontains=q)
            )

        # Basic filters
        city = request.GET.get('city')
        country = request.GET.get('country')
        if city:
            qs = qs.filter(city__iexact=city)
        if country:
            qs = qs.filter(country__iexact=country)

        availability = request.GET.get('availability_status')
        if availability:
            qs = qs.filter(availability_status__iexact=availability)

        rental_type = request.GET.get('rental_type')
        if rental_type:
            qs = qs.filter(rental_type__iexact=rental_type)

        # Price range
        price_min = request.GET.get('price_min')
        price_max = request.GET.get('price_max')
        if price_min:
            try:
                qs = qs.filter(price__gte=float(price_min))
            except ValueError:
                pass
        if price_max:
            try:
                qs = qs.filter(price__lte=float(price_max))
            except ValueError:
                pass

        # Amenities boolean filters (example: is_wifi=true)
        for flag in [
            'is_wifi', 'is_parking', 'is_storage', 'is_mirror', 'is_sink', 'is_styling_chair', 'is_product_shelves', 'is_access_24_hours'
        ]:
            val = request.GET.get(flag)
            if val is not None:
                if str(val).lower() in ('1', 'true', 'yes'):
                    qs = qs.filter(**{flag: True})
                elif str(val).lower() in ('0', 'false', 'no'):
                    qs = qs.filter(**{flag: False})

        # Location-based bounding box + optional radius filter
        lat = request.GET.get('lat')
        lng = request.GET.get('lng')
        radius_km = request.GET.get('radius_km')
        distance_map = {}
        if lat and lng:
            try:
                lat_f = float(lat)
                lng_f = float(lng)
                if radius_km:
                    r_km = float(radius_km)
                else:
                    r_km = None

                # approximate bounding box to reduce result set (1 deg lat ~111 km)
                delta = (r_km / 111.0) if r_km else 1.0
                qs = qs.filter(latitude__isnull=False, longitude__isnull=False)
                qs = qs.filter(latitude__gte=lat_f - delta, latitude__lte=lat_f + delta,
                               longitude__gte=lng_f - delta, longitude__lte=lng_f + delta)

                # compute haversine distances in Python for the remaining items if radius specified
                if r_km is not None:
                    from math import radians, sin, cos, sqrt, atan2

                    def haversine(a_lat, a_lng, b_lat, b_lng):
                        R = 6371.0
                        dlat = radians(b_lat - a_lat)
                        dlng = radians(b_lng - a_lng)
                        a = sin(dlat/2)**2 + cos(radians(a_lat)) * cos(radians(b_lat)) * sin(dlng/2)**2
                        c = 2 * atan2(sqrt(a), sqrt(1-a))
                        return R * c

                    filtered = []
                    for obj in qs:
                        try:
                            d = haversine(lat_f, lng_f, float(obj.latitude), float(obj.longitude))
                        except Exception:
                            continue
                        if d <= r_km:
                            distance_map[obj.pk] = d
                            filtered.append(obj.pk)
                    qs = qs.filter(pk__in=filtered)

            except ValueError:
                pass

        # Sorting
        sort = request.GET.get('sort')
        if sort == 'price_asc':
            qs = qs.order_by('price')
        elif sort == 'price_desc':
            qs = qs.order_by('-price')
        elif sort == 'newest':
            qs = qs.order_by('-create_at')
        elif sort == 'distance' and distance_map:
            # maintain order by distance_map
            ordered_pks = sorted(distance_map.keys(), key=lambda k: distance_map[k])
            preserved = models.Case(*[models.When(pk=pk, then=pos) for pos, pk in enumerate(ordered_pks)])
            qs = qs.filter(pk__in=ordered_pks).order_by(preserved)
        else:
            qs = qs.order_by('-create_at')

        paginator = CustomPagination()
        page = paginator.paginate_queryset(qs, request, view=self)
        serializer = ListingPublicSerializer(page, many=True, context={"request": request})

        data = serializer.data
        # attach distance values if computed
        if distance_map:
            for item in data:
                pk = item.get('id')
                if pk in distance_map:
                    item['distance_km'] = round(distance_map[pk], 3)

        return paginator.get_paginated_response(data)