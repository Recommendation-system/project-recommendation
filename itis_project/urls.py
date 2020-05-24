from django.conf.urls import url
from django.views.generic.base import RedirectView
from django.urls import include
from django.contrib import admin
from django.urls import path

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='content/feed/')),
    path('content/', include("itis_project.apps.content.urls")),
    path('auth/', include("itis_project.apps.authorization.urls")),
    path('admin/', admin.site.urls),
]
