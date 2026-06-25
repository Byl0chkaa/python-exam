from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.dealerships.models import DealershipEmployeeModel, DealershipModel
from apps.dealerships.serializer import (DealershipEmployeeSerializer,
                                         DealershipSerializer)


class DealershipListCreateApiView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = DealershipModel.objects.all()
    serializer_class = DealershipSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        dealership = serializer.save()
        DealershipEmployeeModel.objects.create(
            user=self.request.user,
            dealership=dealership,
            role=DealershipEmployeeModel.LocalRoleChoices.OWNER
        )


class DealershipRetrieveUpdateDestroyApiView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = DealershipModel.objects.all()
    serializer_class = DealershipSerializer
    permission_classes = (IsAuthenticated,)

    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)

        if request.method not in ['GET', 'HEAD', 'OPTIONS']:
            is_owner = DealershipEmployeeModel.objects.filter(
                user=request.user,
                dealership=obj,
                role=DealershipEmployeeModel.LocalRoleChoices.OWNER
            ).exists()

            if not is_owner and not request.user.is_staff:
                raise PermissionDenied(
                    "Тільки власник автосалону або адміністратор платформи може змінювати його дані.")


class DealershipEmployeeListCreateApiView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = DealershipEmployeeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return DealershipEmployeeModel.objects.filter(dealership_id=self.kwargs['dealership_id'])

    def perform_create(self, serializer):
        dealership_id = self.kwargs['dealership_id']

        is_owner = DealershipEmployeeModel.objects.filter(
            user=self.request.user,
            dealership_id=dealership_id,
            role=DealershipEmployeeModel.LocalRoleChoices.OWNER
        ).exists()

        if not is_owner and not self.request.user.is_staff:
            raise PermissionDenied("Ви не можете керувати персоналом цього автосалону.")

        serializer.save(dealership_id=dealership_id)