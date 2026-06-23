import os

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from apps.catalog.models import (BodyTypeModel, BrandModel, CarModelModel,
                                 CityModel, FuelTypeModel, TransmissionModel)
from apps.dealerships.models import DealershipModel


def car_image_upload_path(instance, filename):
    return os.path.join('car_images', f'ad_{instance.car_ad.id}', filename)


class ExchangeRatesModel(models.Model):
    currency = models.CharField(max_length=3, unique=True)
    rate_to_uah = models.DecimalField(max_digits=10, decimal_places=4)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.currency}: {self.rate_to_uah} UAH ({self.updated_at.date()})"


class CarAdModel(models.Model):
    class StatusChoices(models.TextChoices):
        ACTIVE = 'Active', 'Активне'
        PENDING_CHECK = 'Pending', 'Очікує перевірки'
        REJECTED = 'Rejected', 'Відхилено'
        MANAGER_REVIEW = 'Manager_review', 'На перевірці у менеджера'

    class CurrencyChoices(models.TextChoices):
        USD = 'USD', 'Долар США'
        EUR = 'EUR', 'Євро'
        UAH = 'UAH', 'Гривня'

    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ads')
    dealership = models.ForeignKey(DealershipModel, on_delete=models.CASCADE, related_name='ads', null=True, blank=True)
    brand = models.ForeignKey(BrandModel, on_delete=models.PROTECT)
    car_model = models.ForeignKey(CarModelModel, on_delete=models.PROTECT)
    body_type = models.ForeignKey(BodyTypeModel, on_delete=models.PROTECT)
    fuel_type = models.ForeignKey(FuelTypeModel, on_delete=models.PROTECT)
    transmission = models.ForeignKey(TransmissionModel, on_delete=models.PROTECT)
    city = models.ForeignKey(CityModel, on_delete=models.PROTECT)

    year = models.PositiveIntegerField()
    mileage = models.PositiveIntegerField()
    description = models.TextField()

    original_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    original_currency = models.CharField(max_length=3, choices=CurrencyChoices.choices)

    price_usd = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    price_eur = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    price_uah = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    exchange_rate_used = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)

    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING_CHECK)
    edit_attempts = models.PositiveSmallIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.brand.name} {self.car_model.name} - {self.original_price} {self.original_currency}"


class CarImageModel(models.Model):
    car_ad = models.ForeignKey(CarAdModel, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=car_image_upload_path)

    def __str__(self):
        return f"Фото для оголошення {self.car_ad.id}"


class ForbiddenWordModel(models.Model):
    word = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.word


class AdViewModel(models.Model):
    ad = models.ForeignKey(CarAdModel, on_delete=models.CASCADE, related_name='views')
    viewer_ip = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Перегляд для оголошення {self.ad.id} о {self.created_at}"
