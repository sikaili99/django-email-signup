from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.models import update_last_login
from rest_framework.validators import UniqueValidator
from django.utils.text import gettext_lazy as _
from rest_framework import serializers
from accounts.models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):

    phonenumber = serializers.CharField(required=True, validators=[
                                        UniqueValidator(queryset=CustomUser.objects.all())])

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True,)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = (
            'phonenumber',
            'email',
            'first_name',
            'last_name',
            'password',
            'password2',
        )
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'email': {'required': False},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match"})

        if len(attrs['password']) < 6:
            raise serializers.ValidationError(
                {"password": "Password should be 6 charecters long at least"})

        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create(
            phonenumber=validated_data['phonenumber'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class Accountserializer(serializers.ModelSerializer):
    """Get user details"""
    class Meta:
        model = CustomUser
        fields = [
            'phonenumber',
            'is_superuser',
            'address',
            'email',
            'first_name',
            'last_name',
        ]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = CustomUser.USERNAME_FIELD

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        user = CustomUser.objects.filter(pk=self.user.id).first()
        if user:
            # use user serelizer or parse required fields
            data['user'] = Accountserializer(user, many=False).data
        return data


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': _('Token is invalid or expired')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')
