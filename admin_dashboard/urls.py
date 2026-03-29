
from django.urls import path
from .views import ListingAdminView, ListingAdminViewFilters


urlpatterns = [
    path('listings/', ListingAdminViewFilters.as_view(), name="listings"),
    path('listings/<int:pk>/', ListingAdminView.as_view(), name="listings-details"),

]
