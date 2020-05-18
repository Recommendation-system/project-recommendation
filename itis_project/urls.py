from django.conf.urls import url
from django.views.generic.base import RedirectView
from django.urls import include
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='test/feed/')),
    path('test/', include("itis_project.apps.content.urls")),
    path('auth/', include("itis_project.apps.authorization.urls")),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
