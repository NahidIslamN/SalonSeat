from django.urls import path
from .views import SubscribtionPlansView


urlpatterns = [
    path("plans/", SubscribtionPlansView.as_view(), name='subscribtion-plans')
]