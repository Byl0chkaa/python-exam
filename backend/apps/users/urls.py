from django.urls import path

from apps.users.views import ManagerCreateApiView, UserProfileApiView

urlpatterns = [
    path('profile/', UserProfileApiView.as_view(), name='user-profile'),
    path('managers/', ManagerCreateApiView.as_view(), name='create-manager'),
]
