from django.urls import path
from django.http import HttpResponse
from .views import CreateUserView, UsersViewSet, CustomAuth, IncrementWinsView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

urlpatterns = [
    path('increment-wins/', IncrementWinsView.as_view(), name='increment-wins'),
    path('create-user/', CreateUserView.as_view(), name='create_user'),
    path('get-user/', UsersViewSet.as_view(), name='get_user'),
]