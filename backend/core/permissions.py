from rest_framework.permissions import SAFE_METHODS, BasePermission

from apps.users.models import UserModel


class IsAdOwnerOrDealershipStaff(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if not obj.dealership:
            return obj.seller == request.user or request.user.is_staff
        employee = obj.dealership.employees.filter(user=request.user).first()
        if employee and employee.role in ['Owner', 'Sales']:
            return True
        return request.user.is_staff


class IsPremiumUser(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.account_type == UserModel.AccountTypeChoices.PREMIUM
        )


class IsAdminRole(BasePermission):
    def has_permission(self, request, view):

        return bool(
            request.user
            and request.user.is_authenticated
            and (
                request.user.role == UserModel.RoleChoices.ADMIN
                or request.user.is_superuser
            )
        )


class IsManagerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and (
                request.user.role in [UserModel.RoleChoices.MANAGER, UserModel.RoleChoices.ADMIN]
                or request.user.is_superuser
            )
        )
class IsSellerOrDealershipStaff(BasePermission):
    """ Забороняє Покупцям (Buyer) створювати оголошення """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not request.user or not request.user.is_authenticated:
            return False
        if hasattr(request.user, 'role') and request.user.role == UserModel.RoleChoices.BUYER:
            return False
        return True

class IsPremiumAdOwner(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.account_type == UserModel.AccountTypeChoices.PREMIUM
        )

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.role in [UserModel.RoleChoices.ADMIN, UserModel.RoleChoices.MANAGER]:
            return True
        return obj.seller == request.user