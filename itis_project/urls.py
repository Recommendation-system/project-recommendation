from django.urls import include
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('test/', include("itis_project.apps.social_network.urls")),
    path('auth/', include("itis_project.apps.authorization.urls")),
    path('admin/', admin.site.urls),
]
