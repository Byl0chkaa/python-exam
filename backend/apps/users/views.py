from core.permissions import IsAdminRole
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
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