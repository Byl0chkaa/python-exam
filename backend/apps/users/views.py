from core.permissions import IsAdminRole
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.generics import (CreateAPIView, RetrieveUpdateAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.auth.serializers import UserRegisterSerializer
from apps.users.models import UserModel
from apps.users.serializers import ManagerCreateSerializer, UserSerializer


class UserProfileApiView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ManagerCreateApiView(CreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = ManagerCreateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAdminRole,)

    def perform_create(self, serializer):
        serializer.save(role=UserModel.RoleChoices.MANAGER)

class AccountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('account_type',)

class UpgradeAccountApiView(UpdateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = AccountTypeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAdminRole,)
    http_method_names = ['patch']

class AdminChangeUserRoleApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAdminRole,)

    def patch(self, request, pk):
        user_to_modify = get_object_or_404(UserModel, pk=pk)
        new_role = request.data.get('role')

        if new_role not in UserModel.RoleChoices.values:
            return Response(
                {'detail': f'Невалідна роль. Допустимі значення: {UserModel.RoleChoices.values}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user_to_modify.role = new_role
        user_to_modify.save()

        return Response({
            'detail': f'Роль користувача {user_to_modify.email} успішно змінено на {new_role}.'
        }, status=status.HTTP_200_OK)