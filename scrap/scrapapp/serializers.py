from rest_framework import serializers
from scrapapp.models import Ads, Product


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ads
        exclude = []


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = []
