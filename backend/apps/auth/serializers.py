from django.contrib.auth import get_user_model
from django.db.transaction import atomic
from rest_framework import serializers

from apps.users.models import ProfileModel
from apps.users.serializers import ProfileSerializer

UserModel = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = UserModel
        fields = ('id', 'email', 'password', 'username', 'profile')

        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    @atomic
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = UserModel(**validated_data)
        user.set_password(password)
        user.save()
        ProfileModel.objects.create(user=user, **profile_data)

        return user


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['password']
