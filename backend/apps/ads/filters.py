from django_filters import rest_framework as filters

from apps.ads.models import CarAdModel


class AddsFilter(filters.FilterSet):
    price_filter = filters.RangeFilter(field_name='original_price')
    year_filter = filters.RangeFilter(field_name='year')
    brand_filter = filters.CharFilter(field_name='brand__name', lookup_expr='icontains')
    city_filter = filters.CharFilter(field_name='city__name', lookup_expr='icontains')

    class Meta:
        model = CarAdModel
        fields = ('year', 'brand', 'city')
