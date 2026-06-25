from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.catalog.models import (BodyTypeModel, BrandModel, CarModelModel,
                                 CityModel, FuelTypeModel,
                                 MissingBrandRequestModel, RegionModel,
                                 TransmissionModel)
from apps.catalog.serializers import (BodyTypeSerializer, BrandSerializer,
                                      CarModelModelSerializer, CitySerializer,
                                      FuelTypeSerializer,
                                      MissingBrandRequestSerializer,
                                      RegionSerializer, TransmissionSerializer)


class BrandListApiView(ListAPIView):
    queryset = BrandModel.objects.all()
    serializer_class = BrandSerializer
    permission_classes = (AllowAny,)


class CarModelListApiView(ListAPIView):
    queryset = CarModelModel.objects.all()
    serializer_class = CarModelModelSerializer
    permission_classes = (AllowAny,)


class BodyTypeListApiView(ListAPIView):
    queryset = BodyTypeModel.objects.all()
    serializer_class = BodyTypeSerializer
    permission_classes = (AllowAny,)


class FuelTypeListApiView(ListAPIView):
    queryset = FuelTypeModel.objects.all()
    serializer_class = FuelTypeSerializer
    permission_classes = (AllowAny,)


class TransmissionListApiView(ListAPIView):
    queryset = TransmissionModel.objects.all()
    serializer_class = TransmissionSerializer
    permission_classes = (AllowAny,)

class RegionListApiView(ListAPIView):
    queryset = RegionModel.objects.all()
    serializer_class = RegionSerializer
    permission_classes = (AllowAny,)


class CityListApiView(ListAPIView):
    queryset = CityModel.objects.all()
    serializer_class = CitySerializer
    permission_classes = (AllowAny,)

class MissingBrandRequestCreateApiView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = MissingBrandRequestModel.objects.all()
    serializer_class = MissingBrandRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
