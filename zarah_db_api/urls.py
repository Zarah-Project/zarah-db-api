from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from zarah_db_api import settings

urlpatterns = [
    path('v1/authority/', include('authority_list.urls', namespace='authority-list-v1')),
    path('v1/document/', include('document.urls', namespace='document-v1')),
    path('v1/metadata/', include('metadata.urls', namespace='metadata-v1')),

    path('fp/', include('django_drf_filepond.urls')),
    path('admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)\
  + static(settings.MEDIA_URL, document_root=settings.DJANGO_DRF_FILEPOND_FILE_STORE_PATH)
