from django.urls import path
from django.http import HttpResponse


# Создаем функцию-заглушку, которая возвращает пустой ответ
def placeholder_view(request):
    return HttpResponse("Placeholder")


# Объявляем urlpatterns с маршрутом-заглушкой
urlpatterns = [
    path('', placeholder_view, name='placeholder'),  # Заглушка по основному пути
]
