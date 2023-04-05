from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from config import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/', include('config.routes')),
    re_path('', include('social_django.urls', namespace='social'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
