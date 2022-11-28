from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework import generics, views
from accounts.models import CustomUser, Profile
from accounts.serializers import (
    Accountserializer,
    CustomTokenObtainPairSerializer,
    RefreshTokenSerializer,
    RegisterSerializer,
    ProfileSerializer,)

class ListUsersView(views.APIView):

    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            users = CustomUser.objects.all()
            serializer = Accountserializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "success", "error": "You have not been authorized accesss"}, status=status.HTTP_200_OK)


class EmailTokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = CustomTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

class LogoutView(generics.GenericAPIView):
    serializer_class = RefreshTokenSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, *args):
        sz = self.get_serializer(data=request.data)
        sz.is_valid(raise_exception=True)
        sz.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileView(views.APIView):

    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            return Response(data={"meesage": "User not found"},status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk, format=None):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=ProfileSerializer)
    def put(self, request, pk, format=None):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ValidateEmailToken(views.APIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
     operation_description="Post request to include token filed {'token': 'token'}"
     )
    def post(self, request, *args, **kwargs):
        token = request.data.get('token')
        res = {
            'status': 'success',
            'message': 'Valid',
        }
        
        if CustomUser.objects.filter(email_verified_hash=token, email_verified=0).exists():
            tokenExists = CustomUser.objects.get(email_verified_hash=token, email_verified=0)
            tokenExists.email_verified = True
            tokenExists.email_verified = True
            tokenExists.save()

        else:
            res = {
                'status': 'failed',
                'message': 'Invalid',
            }
        
        return Response(res, status=status.HTTP_201_CREATED)