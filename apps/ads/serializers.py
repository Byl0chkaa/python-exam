from django.db.transaction import atomic
from rest_framework import serializers

from apps.ads.models import CarAdModel


class CarAdSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarAdModel
        fields = ('id', 'seller', 'brand', 'car_model', 'description', 'region', 'original_price', 'original_currency',
                  'price_usd', 'price_eur', 'price_uah', 'exchange_rate_used', 'status', 'edit_attempts', 'created_at')
        read_only_fields = ('status', 'edit_attempts', 'price_usd', 'price_eur', 'price_uah', 'exchange_rate_used',
                            'seller')


@atomic
def create(self, validated_data: dict):
    request = self.context.get('request')
    validated_data['seller'] = request.user


    car_ad = CarAdModel.objects.create(**validated_data)

    return car_ad


