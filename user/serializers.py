from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """
    CustomUser table serializer
    """

    class Meta:
        model = CustomUser
        exclude = ('password', 'last_login', 'date_joined', 'user_permissions', 'is_staff', 'is_active')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Token return extension
    """

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['user'] = CustomUserSerializer(self.user, many=False).data

        return data
