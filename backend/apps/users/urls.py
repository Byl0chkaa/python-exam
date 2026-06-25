from django.urls import path

from apps.users.views import (AdminChangeUserRoleApiView, ManagerCreateApiView,
                              UpgradeAccountApiView, UserProfileApiView)

urlpatterns = [
    path('profile/', UserProfileApiView.as_view(), name='user-profile'),
    path('managers/', ManagerCreateApiView.as_view(), name='user-create-manager'),
    path('<int:pk>/upgrade/', UpgradeAccountApiView.as_view(), name='user-upgrade-account'),
    path('<int:pk>/change-role/', AdminChangeUserRoleApiView.as_view(), name='user-admin-change-role'),
]
