from decimal import Decimal

from apps.ads.models import CarAdModel, ForbiddenWordModel
from apps.ads.tasks import validate_ad_description
from apps.catalog.models import (BodyTypeModel, BrandModel, CarModelModel,
                                 CityModel, FuelTypeModel, RegionModel,
                                 TransmissionModel)
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

UserModel = get_user_model()


class AutoRiaCoreTestCase(APITestCase):
    def setUp(self):
        self.brand = BrandModel.objects.create(name='BMW')
        self.car_model = CarModelModel.objects.create(brand=self.brand, name='X5')
        self.body_type = BodyTypeModel.objects.create(name='Sedan')
        self.fuel_type = FuelTypeModel.objects.create(name='Petrol')
        self.transmission = TransmissionModel.objects.create(name='Automatic')
        self.region = RegionModel.objects.create(name='Київська область')
        self.city = CityModel.objects.create(region=self.region, name='Київ')

        self.basic_user = UserModel.objects.create_user(
            email='basic@test.com', username='basic_seller', password='Password123!',
            account_type=UserModel.AccountTypeChoices.BASIC, role=UserModel.RoleChoices.SELLER
        )
        self.premium_user = UserModel.objects.create_user(
            email='premium@test.com', username='premium_seller', password='Password123!',
            account_type=UserModel.AccountTypeChoices.PREMIUM, role=UserModel.RoleChoices.SELLER
        )
        self.buyer_user = UserModel.objects.create_user(
            email='buyer@test.com', username='buyer_user', password='Password123!',
            account_type=UserModel.AccountTypeChoices.BASIC, role=UserModel.RoleChoices.BUYER
        )

        self.valid_ad_data = {
            "brand": "BMW", "car_model": "X5", "body_type": "Sedan",
            "fuel_type": "Petrol", "transmission": "Automatic", "city": "Київ",
            "year": 2021, "mileage": 30000, "description": "Продам чудовий автомобіль в ідеальному стані.",
            "original_price": "25000.00", "original_currency": "USD"
        }

    def test_buyer_cannot_create_ad(self):
        """Перевірка, що користувач із роллю BUYER не може створювати оголошення"""
        self.client.force_authenticate(user=self.buyer_user)
        url = reverse('ads-list-create')
        response = self.client.post(url, self.valid_ad_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_basic_user_ad_creation_limit(self):
        """Перевірка обмеження створення оголошень для Basic акаунтів (макс 1)"""
        self.client.force_authenticate(user=self.basic_user)
        url = reverse('ads-list-create')

        response = self.client.post(url, self.valid_ad_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(url, self.valid_ad_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Перейдіть на Premium', response.data[0])

    def test_premium_user_unlimited_ads(self):
        """Перевірка відсутності лімітів для Premium акаунтів"""
        self.client.force_authenticate(user=self.premium_user)
        url = reverse('ads-list-create')

        for _ in range(3):
            response = self.client.post(url, self.valid_ad_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)



    def test_profanity_moderation_flow(self):
        """Перевірка автоматичної стейт-машини нецензурної лексики"""
        ForbiddenWordModel.objects.create(word='шахрай')

        bad_data = self.valid_ad_data.copy()
        bad_data['description'] = "Цей продавець повний шахрай, не купуйте."

        self.client.force_authenticate(user=self.premium_user)
        url = reverse('ads-list-create')
        response = self.client.post(url, bad_data, format='json')
        ad_id = response.data['id']

        validate_ad_description(ad_id)
        ad = CarAdModel.objects.get(id=ad_id)
        self.assertEqual(ad.status, CarAdModel.StatusChoices.PENDING_CHECK)
        self.assertEqual(ad.edit_attempts, 1)

        validate_ad_description(ad_id)
        validate_ad_description(ad_id)

        ad.refresh_from_db()
        self.assertEqual(ad.status, CarAdModel.StatusChoices.MANAGER_REVIEW)

    def test_premium_statistics_privacy(self):
        """Перевірка, що Premium користувач не може дивитися статистику чужих оголошень"""
        ad = CarAdModel.objects.create(
            seller=self.basic_user, brand=self.brand, car_model=self.car_model,
            body_type=self.body_type, fuel_type=self.fuel_type, transmission=self.transmission,
            city=self.city, year=2020, mileage=10000, description="Test",
            original_price=Decimal("100.00"), original_currency="USD"
        )

        self.client.force_authenticate(user=self.premium_user)
        url = reverse('ads-statistics', kwargs={'pk': ad.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)