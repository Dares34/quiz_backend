"""
URL configuration for quiz_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_yasg.openapi import Parameter, TYPE_STRING, IN_HEADER
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
import debug_toolbar


schema_view = get_schema_view(
    openapi.Info(
        title="Мой API",
        default_version='v1',
        description="Заклинание",
    ),
    public=True,
    authentication_classes=[TokenAuthentication],
    permission_classes=[IsAuthenticated],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('api/', include('rest_api.urls')),

    path('__debug__/', include(debug_toolbar.urls)),
    # path('api/rooms/', include('room.urls')),
    # path('api/users/', include('user.urls')),
    # path('api/invitations/', include('invitation.urls')),
    # path('api/quizzes', include('quiz.urls')),
    # path('api/rooms_test/', include("room.urls")),
]
