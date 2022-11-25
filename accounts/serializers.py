import uuid
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.validators import UniqueValidator
from django.utils.text import gettext_lazy as _
from rest_framework import serializers
from accounts.models import CustomUser, Profile
from .send_email import send_email_verify


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
            'email_verified_hash',
        )
        extra_kwargs = {
            'email_verified_hash': {'required': False},
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
        if CustomUser.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError(
                {"email": "Email address is already used."})

        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create(
            phonenumber=validated_data['phonenumber'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        my_uuid = uuid.uuid4()
        email=validated_data['email'],
        first_name=validated_data['first_name'],
        user.email_verified_hash = str(my_uuid)
        user.save()
        send_email_verify(first_name[0],email[0],str(my_uuid))
        return user


class Accountserializer(serializers.ModelSerializer):
    """Get user details"""
    class Meta:
        model = CustomUser
        fields = [
            'phonenumber',
            'is_superuser',
            'is_staff',
            'email_verified',
            'email',
            'first_name',
            'last_name',
            'id',
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


class ProfileSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(source='user')
    user_id = serializers.ReadOnlyField(source='user.id')
    image_url = serializers.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'user_id', 'bio', 'is_public', 'avator']
