from django.contrib.auth.models import AbstractUser
from django.db import models


class UserModel(AbstractUser):
    class Meta:
        db_table = 'users'
        ordering = ['id']

    class RoleChoices(models.TextChoices):
        BUYER = 'Buyer', 'Покупець'
        SELLER = 'Seller', 'Продавець'
        MANAGER = 'Manager', 'Менеждер'
        ADMIN = 'Admin', 'Адміністратор'


    email = models.EmailField(unique=True)
    role = models.CharField(max_length=7, choices=RoleChoices.choices, default=RoleChoices.BUYER)
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class ProfileModel(models.Model):
    class Meta:
        db_table = 'profiles'
        ordering = ['id']

    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    age = models.PositiveIntegerField()
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='profile')
