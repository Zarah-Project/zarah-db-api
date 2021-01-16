from django.urls import path

from webapi.views.search_views import DocumentPublicSearch
from webapi.views.views import DocumentPublicDetail, StoredFilePublicView

app_name = 'webapi'

urlpatterns = [
    path('search', DocumentPublicSearch.as_view(), name='document-public-search'),
    path('document/<int:pk>/', DocumentPublicDetail.as_view(), name='document-detail'),
    path('view_file/<str:id>', StoredFilePublicView.as_view(), name='stored-file-pubic-view'),
]