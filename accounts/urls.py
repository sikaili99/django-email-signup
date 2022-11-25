from rest_framework_simplejwt.views import TokenRefreshView
from accounts.views import (
    EmailTokenObtainPairView, 
    ValidateEmailToken,
    ListUsersView, 
    RegisterView,
    LogoutView, 
    )
from django.urls import path

urlpatterns = [
    path('token/', EmailTokenObtainPairView.as_view()),
    path('email/verify/', ValidateEmailToken.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('users/', ListUsersView.as_view()),
    path('register/', RegisterView.as_view()),
    path('logout/', LogoutView.as_view()),
]
