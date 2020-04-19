from django.urls import include, path
from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('feed/', include("social_network.urls")),
    path('admin/', admin.site.urls),
]
