from rest_framework import serializers
from .models import SubscriptionPlan, Feature


class FeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = "__all__"


class SubscribtionPlanViewSerializer(serializers.ModelSerializer):
    features = FeaturesSerializer(many=True, read_only=True)
    class Meta:
        model = SubscriptionPlan
        fields = "__all__"