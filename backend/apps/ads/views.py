from decimal import Decimal

from core.permissions import (IsAdOwnerOrDealershipStaff, IsManagerOrAdmin,
                              IsPremiumUser, IsSellerOrDealershipStaff, IsPremiumAdOwner)
from core.services.statistic_service import AdStatisticService
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (CreateAPIView, ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.ads.filters import AddsFilter
from apps.ads.models import (AdViewModel, CarAdModel, CarImageModel,
                             ExchangeRatesModel)
from apps.ads.serializers import CarAdSerializer, CarImageSerializer
from apps.ads.tasks import validate_ad_description
from apps.dealerships.models import DealershipEmployeeModel
from apps.users.models import UserModel


class CreateAdApiView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_class = AddsFilter

    permission_classes = (IsAuthenticatedOrReadOnly,IsSellerOrDealershipStaff)
    queryset = CarAdModel.objects.all()
    serializer_class = CarAdSerializer

    def perform_create(self, serializer):
        user: UserModel = self.request.user
        dealership_id = serializer.validated_data.pop('dealership_id', None)
        dealership = None

        if dealership_id:
            employee_record = DealershipEmployeeModel.objects.filter(
                user=user,
                dealership_id=dealership_id
            ).first()

            if not employee_record:
                raise ValidationError("Ви не є працівником вказаного автосалону або такого салону не існує.")
            dealership = employee_record.dealership
        else:
            if user.account_type == UserModel.AccountTypeChoices.BASIC:
                if CarAdModel.objects.filter(seller=user, dealership__isnull=True).count() >= 1:
                    raise ValidationError('Ви вже використали ліміт на 1 оголошення. Перейдіть на Premium.')

        original_price = serializer.validated_data.get('original_price')
        original_currency = serializer.validated_data.get('original_currency')

        try:
            rate_usd = ExchangeRatesModel.objects.get(currency='USD').rate_to_uah
            rate_eur = ExchangeRatesModel.objects.get(currency='EUR').rate_to_uah
        except ExchangeRatesModel.DoesNotExist:
            rate_usd = Decimal('41.5')
            rate_eur = Decimal('45.2')

        if original_currency == 'USD':
            price_usd = original_price
            price_uah = original_price * rate_usd
            price_eur = price_uah / rate_eur if rate_eur != 0 else Decimal('0')
            exchange_rate_used = rate_usd
        elif original_currency == 'EUR':
            price_eur = original_price
            price_uah = original_price * rate_eur
            price_usd = price_uah / rate_usd if rate_usd != 0 else Decimal('0')
            exchange_rate_used = rate_eur
        else:
            price_uah = original_price
            price_usd = original_price / rate_usd if rate_usd != 0 else Decimal('0')
            price_eur = original_price / rate_eur if rate_eur != 0 else Decimal('0')
            exchange_rate_used = rate_usd

        instance = serializer.save(
            seller=user,
            dealership=dealership,
            price_usd=price_usd,
            price_eur=price_eur,
            price_uah=price_uah,
            exchange_rate_used=exchange_rate_used
        )

        validate_ad_description.delay(instance.id)

class UpdateDestroyAdApiView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdOwnerOrDealershipStaff)
    queryset = CarAdModel.objects.all()
    serializer_class = CarAdSerializer

    def get_object(self):
        obj = super().get_object()

        if self.request.method == 'GET':
            client_ip = self.request.META.get('REMOTE_ADDR')
            AdViewModel.objects.create(ad=obj, viewer_ip=client_ip)

        return obj

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.status == CarAdModel.StatusChoices.MANAGER_REVIEW:
            raise ValidationError(
                {'detail': 'Оголошення знаходиться на перевірці у менеджера. Редагування заборонено.'}
            )

        return super().update(request, *args, **kwargs)

    def perform_update(self, serializer):
        instance = serializer.save()

        if 'description' in self.request.data:
            instance.status = CarAdModel.StatusChoices.PENDING_CHECK
            instance.save()
            validate_ad_description.delay(instance.id)


class CreateImageAdApiView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = CarImageModel.objects.all()
    serializer_class = CarImageSerializer

    def perform_create(self, serializer):
        ad_pk = self.kwargs['pk']
        car_ad = get_object_or_404(CarAdModel, pk=ad_pk)
        serializer.save(car_ad=car_ad)


class PremiumAdStatsApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsPremiumAdOwner,)

    def get(self, request, pk, *args, **kwargs):
        ad = get_object_or_404(CarAdModel, pk=pk)
        self.check_object_permissions(request, ad)
        stats_data = AdStatisticService.get_statistic(ad)
        return Response(stats_data)


class AdModerationApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsManagerOrAdmin,)

    def patch(self, request, pk):
        ad = get_object_or_404(CarAdModel, pk=pk)
        new_status = request.data.get('status')

        if new_status not in [CarAdModel.StatusChoices.ACTIVE, CarAdModel.StatusChoices.REJECTED]:
            raise ValidationError({'detail': 'Невалідний статус. Допустимі значення: Active, Rejected'})

        ad.status = new_status
        ad.save()
        return Response({'detail': f'Статус оголошення {pk} змінено на {new_status}.'})