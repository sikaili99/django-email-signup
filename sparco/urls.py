from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Sparco API",
        default_version='v1',
        description="Test description",
        terms_of_service="",
        contact=openapi.Contact(email="sikaili99@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('',
         schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('password_reset/',
         include('django_rest_passwordreset.urls',
                 namespace='password_reset')),
    path('admin/', admin.site.urls),
]
