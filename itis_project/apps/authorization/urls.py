from django.urls import path

from .views import *

urlpatterns = [
    path('login/', LoginInView.as_view(), name='login_in_url'),
    path('logout/', logout, name='logout_url'),
    path('register', RegisterView.as_view(), name='register_url'),
]