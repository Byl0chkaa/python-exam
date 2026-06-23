from django.urls import path

from apps.dealerships.views import (DealershipEmployeeListCreateApiView,
                                    DealershipListCreateApiView,
                                    DealershipRetrieveUpdateDestroyApiView)

urlpatterns = [
    path('', DealershipListCreateApiView.as_view(), name='dealership-list-create'),
    path('<int:pk>/', DealershipRetrieveUpdateDestroyApiView.as_view(), name='dealership-detail'),
    path('<int:dealership_id>/employees/', DealershipEmployeeListCreateApiView.as_view(), name='dealership-employees'),
]