from django.conf import settings
from django.db import models


class BrandModel(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

class BodyTypeModel(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class FuelTypeModel(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class TransmissionModel(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

class RegionModel(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class CityModel(models.Model):
    region = models.ForeignKey(RegionModel, on_delete=models.CASCADE, related_name='cities')
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.region.name})"

class CarModelModel(models.Model):
    brand = models.ForeignKey(BrandModel,on_delete=models.CASCADE)
    name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.brand.name} {self.name}"

class MissingBrandRequestModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    proposed_brand_name = models.CharField(max_length=100)
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)