from django.urls import path
from django.http import HttpResponse

def placeholder_view(request):
    return HttpResponse("Placeholder")

urlpatterns = [
    path('', placeholder_view, name='placeholder'), 
]
