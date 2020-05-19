from django.urls import path, include

from .views import *

urlpatterns = [
    path('home/', home, name='home_url'),
    path('login/', LoginView.as_view(), name='login_url'),
    path('logout/', logout, name='logout_url'),
    path('registration/', RegistrationView.as_view(), name='registration_url'),
    path('vk-auth-check/', vk_auth_check, name='vk-auth-check'),
    path('', include('social_django.urls'), name='auth-with-vk_url'),
]