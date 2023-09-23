from django.urls import path

from .views import Config, ObtainAuthToken, UserCreate

urlpatterns = [
    path('token/obtain', ObtainAuthToken.as_view(), name='token_create'),
    path('signup', UserCreate.as_view(), name='userCreate'),
    path('config', Config.as_view(), name='Config'),

]
