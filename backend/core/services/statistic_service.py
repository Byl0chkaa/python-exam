from datetime import timedelta

from apps.ads.models import AdViewModel, CarAdModel
from django.db.models import Avg
from django.utils import timezone


class AdStatisticService:
    @staticmethod
    def get_statistic(ad: CarAdModel) -> dict:
        now = timezone.now()

        view_qs = AdViewModel.objects.filter(ad=ad)

        total_views = view_qs.count()
        views_today = view_qs.filter(created_at__gte=now - timedelta(days=1)).count()
        views_week = view_qs.filter(created_at__gte=now - timedelta(days=7)).count()
        views_month = view_qs.filter(created_at__gte=now - timedelta(days=30)).count()

        similar_cars_qs = CarAdModel.objects.filter(
            brand=ad.brand,
            car_model=ad.car_model,
            status=CarAdModel.StatusChoices.ACTIVE
        )

        avg_price_ukraine = similar_cars_qs.aggregate(
            Avg('price_usd')
        )['price_usd__avg']

        avg_price_region = similar_cars_qs.filter(
            city__region=ad.city.region
        ).aggregate(
            Avg('price_usd')
        )['price_usd__avg']

        return {
            "views": {
                "total": total_views,
                "today": views_today,
                "week": views_week,
                "month": views_month,
            },
            "average_price_usd": {
                "ukraine": round(avg_price_ukraine, 2) if avg_price_ukraine else 0.0,
                "region": round(avg_price_region, 2) if avg_price_region else 0.0,
                "region_name": ad.city.region.name,
            }
        }