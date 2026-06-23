from rest_framework import serializers

from apps.dealerships.models import DealershipEmployeeModel, DealershipModel


class DealershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealershipModel
        fields = ('id', 'name', 'description', 'created_at')


class DealershipEmployeeSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = DealershipEmployeeModel
        fields = ('id', 'user', 'user_email', 'role', 'role_display')