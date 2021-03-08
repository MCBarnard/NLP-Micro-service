from django.urls import path
from nlp import views

urlpatterns = [
    path('', views.SystemUp.as_view()),
    path('support-query', views.AnswerQuestion.as_view()),
]
