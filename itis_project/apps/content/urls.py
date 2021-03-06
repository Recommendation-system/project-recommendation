from django.conf.urls import url
from django.urls import path
from django.views.generic import RedirectView

from .views import *

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='feed/')),
    path('feed/', feed_list, name='feed_url'),
    path('feed/post/like/', like_post, name='like-post'),
    path('profile/edit/', profile_edit, name='profile-edit_url'),
    path('profile/edit/change_password/', change_password, name='change_password_url'),
    path('profile/', profile, name='profile_url'),
    path('create/post/', create_post, name='create_post_url'),
    path('post/<str:post_slug>/', post_details, name='post_detail_url'),
    path('post/<str:post_slug>/edit/', post_edit, name='post_edit_url'),
]

