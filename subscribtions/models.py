from django.db import models

# Create your models here.

class Feature(models.Model):
    text = models.CharField(max_length=250)

    def __str__(self):
        return self.text


class SubscriptionPlan(models.Model):
    price = models.DecimalField(max_digits=9, decimal_places=2)
    listing_limit = models.IntegerField()
    media_limit = models.IntegerField()
    is_unlimited_listing = models.BooleanField(default=False)
    is_able_analytics = models.BooleanField(default=False)
    features = models.ManyToManyField(Feature, related_name='subscription_plans')

    def __str__(self):
        return f"{self.id}------{self.price}"