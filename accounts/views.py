from rest_framework_simplejwt.views import TokenObtainPairView
from templated_email import send_templated_mail
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework import generics, views
from accounts.models import CustomUser
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

    def post(self, *args, **kwargs):
        serializer = ProfileSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.sav(user=self.request.user)
            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': serializer.errors})


class ValidateEmailToken(views.APIView):
    permission_classes = (permissions.AllowAny,)

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