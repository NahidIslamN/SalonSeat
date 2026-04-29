from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from SalonSeat.custom_permission import IsSalunOwner
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from chats.tasks import sent_note_to_user
from .models import SubscriptionPlan
from SalonSeat.pagination import CustomPagination


# Create your views here.

class SubscribtionPlansView(APIView):
    permission_classes = [IsSalunOwner]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get(self, request):
        plans = SubscriptionPlan.objects.all().order_by("id")
        serializer = SubscribtionPlanViewSerializer(plans, many=True)
        return Response(
            {
                "success":True,
                "message":"data fatched!",
                "plans":serializer.data
            }
        )
