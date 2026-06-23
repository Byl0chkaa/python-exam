from django.urls import path

from apps.ads.views import (AdModerationApiView, CreateAdApiView,
                            CreateImageAdApiView, PremiumAdStatsApiView,
                            UpdateDestroyAdApiView)

urlpatterns = [
    path('', CreateAdApiView.as_view(), name='ads-list-create'),
    path('<int:pk>/', UpdateDestroyAdApiView.as_view(), name='ads-detail'),
    path('<int:pk>/images/', CreateImageAdApiView.as_view(), name='ads-add-image'),
    path('<int:pk>/statistics/', PremiumAdStatsApiView.as_view(), name='ads-statistics'),
    path('<int:pk>/moderate/', AdModerationApiView.as_view(), name='ad-moderate'),
]