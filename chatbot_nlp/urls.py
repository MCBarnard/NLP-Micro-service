from django.urls import path
from nlp import views

urlpatterns = [
    path('', views.SystemUp.as_view()),
    path('ask', views.AnswerQuestion.as_view()),
]
