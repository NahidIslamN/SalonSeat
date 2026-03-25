from django.urls import path
from .views import *

urlpatterns = [
	path('listings/', SalunListingView.as_view(), name='owner-listings'),
	path('listings/<int:pk>/', SalunListingDetailView.as_view(), name='owner-listing-detail'),
	path('media/<int:pk>/', SalunListingMediaDeleteView.as_view(), name='owner-listing-media-delete'),
]
