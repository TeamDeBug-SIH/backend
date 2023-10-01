from django.urls import path

from .views import Brainstorm, Learn, Practice, QuizView

urlpatterns = [
    path('learn', Learn.as_view(), name='Learn'),
    path('brainstorm', Brainstorm.as_view(), name='Brainstorm'),
    path('practice', Practice.as_view(), name='Practice'),
    path('quiz', QuizView.as_view(), name='Quiz'),
]
