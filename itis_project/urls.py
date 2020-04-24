from django.urls import include
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('test/', include("social_network.urls")),
    path('admin/', admin.site.urls),
]
