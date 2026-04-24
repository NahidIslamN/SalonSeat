
from django.urls import path
from .views import ListingViewBeautyProfission


urlpatterns = [
	path('listings/', ListingViewBeautyProfission.as_view(), name='bpes-listings'),
]
