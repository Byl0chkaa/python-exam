from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.users.models import ProfileModel

UserModel = get_user_model()
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileModel
        fields = ('name', 'surname', 'age')


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = UserModel
        fields = ('username', 'email', 'profile')
        extra_kwargs = {
            'password': {'write_only': True},
            'is_premium': {'read_only': True},
            'role': {'read_only': True}
        }

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = UserModel.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        ProfileModel.objects.create(user=user, **profile_data)
        return user

    