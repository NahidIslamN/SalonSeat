from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from SalonSeat.custom_permission import IsProfissional
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from chats.tasks import sent_note_to_user
from jayla_models.models import Listing, Photo_Media
from SalonSeat.pagination import CustomPagination

# Create your views here.
