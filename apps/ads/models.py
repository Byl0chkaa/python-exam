from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from apps.catalog.models import BrandModel, CarModelModel


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
    brand = models.ForeignKey(BrandModel, on_delete=models.PROTECT)
    car_model = models.ForeignKey(CarModelModel, on_delete=models.PROTECT)
    description = models.TextField()
    region = models.CharField(max_length=100)

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


class AdViewModel(models.Model):
    ad = models.ForeignKey(CarAdModel, on_delete=models.CASCADE, related_name='views')
    viewer_ip = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"View for Ad {self.ad.id} at {self.created_at}"