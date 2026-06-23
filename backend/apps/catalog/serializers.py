from rest_framework import serializers

from apps.catalog.models import (BodyTypeModel, BrandModel, CarModelModel,
                                 CityModel, FuelTypeModel,
                                 MissingBrandRequestModel, RegionModel,
                                 TransmissionModel)


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandModel
        fields = ('id', 'name')


class CarModelModelSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source='brand.name', read_only=True)

    class Meta:
        model = CarModelModel
        fields = ('id', 'name', 'brand', 'brand_name')


class BodyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BodyTypeModel
        fields = ('id', 'name')


class FuelTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelTypeModel
        fields = ('id', 'name')


class TransmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransmissionModel
        fields = ('id', 'name')


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegionModel
        fields = ('id', 'name')


class CitySerializer(serializers.ModelSerializer):
    region_name = serializers.CharField(source='region.name', read_only=True)

    class Meta:
        model = CityModel
        fields = ('id', 'name', 'region', 'region_name')


class MissingBrandRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissingBrandRequestModel
        fields = ('id', 'user', 'proposed_brand_name', 'is_resolved', 'created_at')

    read_only_fields = ('is_resolved', 'user')
