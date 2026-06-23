from django.urls import path

from apps.catalog.views import (BodyTypeListApiView, BrandListApiView,
                                CarModelListApiView, CityListApiView,
                                FuelTypeListApiView,
                                MissingBrandRequestCreateApiView,
                                RegionListApiView, TransmissionListApiView)

urlpatterns = [
    # Марки та моделі
    path('brands/', BrandListApiView.as_view(), name='catalog_brand_list'),
    path('car-models/', CarModelListApiView.as_view(), name='catalog_car_model_list'),
    path('body-types/', BodyTypeListApiView.as_view(), name='catalog_body_type_list'),
    path('fuel-types/', FuelTypeListApiView.as_view(), name='catalog_fuel_type_list'),
    path('transmissions/', TransmissionListApiView.as_view(), name='catalog_transmission_list'),
    path('regions/', RegionListApiView.as_view(), name='catalog_region_list'),
    path('cities/', CityListApiView.as_view(), name='catalog_city_list'),
    path('missing-brand-request/', MissingBrandRequestCreateApiView.as_view(), name='catalog_missing_brand_request_create'),
]