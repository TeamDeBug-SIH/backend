from django.urls import path

from .views import Learn, QuizView

urlpatterns = [
    path('learn', Learn.as_view(), name='Learn'),
    path('quiz', QuizView.as_view(), name='Quiz'),
]
