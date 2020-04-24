from django.urls import path

from .views import *


urlpatterns = [
    path('feed/', feed),
    path('login/', login),
    path('register/', register),
]