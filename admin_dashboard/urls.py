
from django.urls import path
from .views import ListingAdminView, ListingAdminViewFilters, UsersAdminView


urlpatterns = [
    path('users/', UsersAdminView.as_view(), name='users'),
    path('users/<int:pk>/', UsersAdminView.as_view(), name='users-detail'),
    path('listings/', ListingAdminViewFilters.as_view(), name="listings"),
    path('listings/<int:pk>/', ListingAdminView.as_view(), name="listings-details"),
]
