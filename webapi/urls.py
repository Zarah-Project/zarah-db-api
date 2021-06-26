from django.urls import path

from webapi.views.search_views import DocumentPublicSearch
from webapi.views.views import DocumentPublicDetail, StoredFilePublicView, DocumentCitation, PersonPublicDetail, \
    OrganisationPublicDetail, EventPublicDetail, PlacePublicDetail

app_name = 'webapi'

urlpatterns = [
    path('search', DocumentPublicSearch.as_view(), name='document-public-search'),
    path('document/<int:pk>/', DocumentPublicDetail.as_view(), name='document-detail'),
    path('view_file/<str:id>', StoredFilePublicView.as_view(), name='stored-file-pubic-view'),
    path('document/citation/<int:pk>', DocumentCitation.as_view(), name='document-citation'),

    path('people/<int:pk>/', PersonPublicDetail.as_view(), name='person-detail'),
    path('organisations/<int:pk>/', OrganisationPublicDetail.as_view(), name='person-detail'),
    path('events/<int:pk>/', EventPublicDetail.as_view(), name='event-detail'),
    path('places/<int:pk>/', PlacePublicDetail.as_view(), name='place-detail'),
]