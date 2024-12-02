from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user.views import UsersViewSet, CreateUserView
from .views import CreateRoomView

router = DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    path('users/', include("user.urls")),
    path('rooms/', include('room.urls')),
    path('quizes/', include('quiz.urls')),
    # path('create_user/', CreateUserView.as_view(), name='create_user'),
    # path('get_user/', UsersViewSet.as_view(), name='get_user'),
    # path('create_room/', CreateRoomView.as_view(), name='create_room'),
    # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
