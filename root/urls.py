from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from root.settings import MEDIA_ROOT, MEDIA_URL, STATIC_ROOT, STATIC_URL, DEBUG

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.urls')),
]
if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
    urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)
