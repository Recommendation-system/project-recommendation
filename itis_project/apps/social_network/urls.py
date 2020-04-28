from django.urls import path

from .views import *

app_name = 'test'

urlpatterns = [
    path('feed/like/', like_post, name='like-post'),
    path('feed/', feed, name='post-list'),
    path('login/', login),
    path('register/', register),
]