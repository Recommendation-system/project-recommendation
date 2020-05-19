from django.urls import path

from .views import *

urlpatterns = [
    path('feed/', feed_list, name='feed_url'),
    path('feed/post/like/', like_post, name='like-post'),
    path('profile/edit/', profile_edit, name='profile-edit_url'),
    path('create/post/', create_post, name='create_post_url'),
    path('post/<str:post_slug>/', post_details, name='post_detail_url'),
    path('post/<str:post_slug>/edit/', post_edit, name='post_edit_url'),
]

