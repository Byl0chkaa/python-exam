from django.db.transaction import atomic
from rest_framework import serializers

from apps.ads.models import CarAdModel, CarImageModel


class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImageModel
        fields = ('id', 'image')


class CarAdSerializer(serializers.ModelSerializer):
    images = CarImageSerializer(many=True, read_only=True)
    dealership_id = serializers.IntegerField(required=False, write_only=True)

    class Meta:
        model = CarAdModel
        fields = (
            'id', 'seller', 'brand', 'dealership_id','dealership','car_model', 'body_type', 'fuel_type',
            'transmission', 'city', 'year', 'mileage', 'description',
            'original_price', 'original_currency', 'price_usd', 'price_eur',
            'price_uah', 'exchange_rate_used', 'status', 'edit_attempts',
            'created_at', 'images'
        )
        read_only_fields = (
            'status', 'edit_attempts', 'price_usd', 'price_eur', 'price_uah',
            'exchange_rate_used','dealership', 'seller'
        )

    @atomic
    def create(self, validated_data: dict):
        request = self.context.get('request')
        validated_data['seller'] = request.user

        car_ad = CarAdModel.objects.create(**validated_data)

        return car_ad
