from django.urls import path

from apps.catalog.views import BrandListApiView, CarModelListApiView, MissingBrandRequestCreateApiView

urlpatterns = [
    path('brand_list/', BrandListApiView.as_view(), name='catalog_brand_list'),
    path('car_list/', CarModelListApiView.as_view(), name='catalog_car_list'),
    path('missing_brand_request_create/', MissingBrandRequestCreateApiView.as_view(), name='catalog_missing_brand_request_create'),
]