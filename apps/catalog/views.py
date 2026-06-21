from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.catalog.models import BrandModel, CarModelModel, MissingBrandRequestModel
from apps.catalog.serializers import BrandSerializer, CarModelModelSerializer, MissingBrandRequestSerializer


class BrandListApiView(ListAPIView):
    queryset = BrandModel.objects.all()
    serializer_class = BrandSerializer


class CarModelListApiView(ListAPIView):
    queryset = CarModelModel.objects.all()
    serializer_class = CarModelModelSerializer


class MissingBrandRequestCreateApiView(CreateAPIView):
    queryset = MissingBrandRequestModel.objects.all()
    serializer_class = MissingBrandRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
