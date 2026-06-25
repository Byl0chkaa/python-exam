import secrets

from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.users.models import ProfileModel

UserModel = get_user_model()


class ManagerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('email', 'username')

    def create(self, validated_data):
        password = secrets.token_urlsafe(12)
        user = UserModel.objects.create_user(
            **validated_data,
            password=password,
        )

        ProfileModel.objects.create(
            user=user,
            name=validated_data.get('username', 'Manager'),
            surname='',
            age=18,
        )
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileModel
        fields = ('name', 'surname', 'age')


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = UserModel
        fields = ('id', 'email', 'role', 'account_type', 'profile')
        read_only_fields = ('id', 'email', 'role', 'account_type')

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if profile_data:
            profile, _ = ProfileModel.objects.get_or_create(
                user=instance,
                defaults={'name': '', 'surname': '', 'age': 18}
            )
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        return instance