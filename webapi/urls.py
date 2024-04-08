from django.conf.urls import url
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from webapi.views.search_views import DocumentPublicSearch
from webapi.views.views import DocumentPublicDetail, StoredFilePublicView, DocumentCitation, PersonPublicDetail, \
    OrganisationPublicDetail, EventPublicDetail, PlacePublicDetail, DocumentsBySpecialRecord

app_name = 'webapi'

schema_view = get_schema_view(
   openapi.Info(
      title="Zarah DV Web API",
      default_version='v1',
      description="Zarah DB REST API Public Endpoints",
      contact=openapi.Contact(email="bonej@ceu.edu"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,)
)

urlpatterns = [
    path('search', DocumentPublicSearch.as_view(), name='document-public-search'),
    path('document/<int:pk>/', DocumentPublicDetail.as_view(), name='document-detail'),
    path('view_file/<str:id>', StoredFilePublicView.as_view(), name='stored-file-pubic-view'),
    path('document/citation/<int:pk>', DocumentCitation.as_view(), name='document-citation'),

    path('people/<int:pk>/', PersonPublicDetail.as_view(), name='person-detail'),
    path('organisations/<int:pk>/', OrganisationPublicDetail.as_view(), name='person-detail'),
    path('events/<int:pk>/', EventPublicDetail.as_view(), name='event-detail'),
    path('places/<int:pk>/', PlacePublicDetail.as_view(), name='place-detail'),

    path('document-by/<str:type>/<int:pk>', DocumentsBySpecialRecord.as_view(), name='document-by-special-record'),

    # url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]