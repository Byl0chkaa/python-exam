from django.db import models
from django.conf import settings

class BrandModel(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

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