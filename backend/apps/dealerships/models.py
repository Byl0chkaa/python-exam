from django.conf import settings
from django.db import models


class DealershipModel(models.Model):
    name = models.CharField(max_length=15, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class DealershipEmployeeModel(models.Model):
    class LocalRoleChoices(models.TextChoices):
        OWNER = 'Owner', 'Власник'
        SALES = 'Sales', 'Менеджер з продажу'
        MECHANIC = 'Mechanic', 'Механік'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='dealership_roles')
    dealership = models.ForeignKey(DealershipModel, on_delete=models.CASCADE, related_name='employees')
    role = models.CharField(max_length=20, choices=LocalRoleChoices.choices)

    class Meta:
        unique_together = ('user', 'dealership')

    def __str__(self):
        return f"{self.user.email} - {self.get_role_display()} in {self.dealership.name}"