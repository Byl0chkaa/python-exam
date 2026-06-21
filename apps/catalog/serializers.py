from rest_framework import serializers

from apps.catalog.models import BrandModel, CarModelModel, MissingBrandRequestModel


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandModel
        fields = ('id', 'name')

class CarModelModelSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source='brand.name', read_only=True)

    class Meta:
        model = CarModelModel
        fields = ('id', 'name', 'brand', 'brand_name')


class MissingBrandRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissingBrandRequestModel
        fields = ('id', 'user', 'proposed_brand_name', 'is_resolved', 'created_at')

    read_only_fields = ('is_resolved', 'user')