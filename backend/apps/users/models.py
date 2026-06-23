from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.users.managers import UserManager


class UserModel(AbstractUser):
    class Meta:
        db_table = 'users'
        ordering = ['id']

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
    )

    class RoleChoices(models.TextChoices):
        BUYER = 'Buyer', 'Покупець'
        SELLER = 'Seller', 'Продавець'
        MANAGER = 'Manager', 'Менеждер'
        ADMIN = 'Admin', 'Адміністратор'

    class AccountTypeChoices(models.TextChoices):
        BASIC = 'Basic', 'Базовий'
        PREMIUM = 'Premium', 'Преміум'

    account_type = models.CharField(max_length=10, choices=AccountTypeChoices.choices, default=AccountTypeChoices.BASIC)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=7, choices=RoleChoices.choices, default=RoleChoices.BUYER)

    objects = UserManager()

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"


class ProfileModel(models.Model):
    class Meta:
        db_table = 'profiles'
        ordering = ['id']

    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    age = models.PositiveIntegerField()
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='profile')
