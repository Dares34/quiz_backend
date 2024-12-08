from django.urls import path
from django.http import HttpResponse
from .views import CreateQuizQuestionsView
urlpatterns = [
    path('create-question', CreateQuizQuestionsView.as_view(), name = "question-create"),
]