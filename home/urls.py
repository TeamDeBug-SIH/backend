from django.urls import path

from .views import Learn, QuizView
from rest_framework_simplejwt import views as jwt_views
urlpatterns = [
    path('learn', Learn.as_view(), name='Learn'),
    path('quiz', QuizView.as_view(), name='Quiz'),
    path(
        "api/token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path(
        "api/token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"
    ),
]
