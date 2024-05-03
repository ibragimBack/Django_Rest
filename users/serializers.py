from rest_framework import serializers
from . models import CustomUser, ConfirmationCode
from rest_framework.exceptions import ValidationError

class UserAbstractSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserAuthorizationSerializer(UserAbstractSerializer):
    pass


class UserRegistrationSerializer(UserAbstractSerializer):
    def validate_username(self, username):
        try:
            CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return username
        raise ValidationError('User already exists!')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = 'username password'


class ConfirmationCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfirmationCode
        fields = ['code']