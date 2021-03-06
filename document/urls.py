from django.urls import path

from document.views.search_views import DocumentSearch
from document.views.views import DocumentList, DocumentDetail, DocumentPublicList, DocumentPublicDetail, DocumentClone
from document.views.file_views import TemporaryFileStoreView, StoredFileRemoveView, StoredFileView

app_name = 'document'

urlpatterns = [
    path('', DocumentList.as_view(), name='document-list'),
    path('search', DocumentSearch.as_view(), name='document-search'),
    path('<int:pk>/', DocumentDetail.as_view(), name='document-detail'),
    path('clone/<int:pk>/', DocumentClone.as_view(), name='document-clone'),

    path('store_file/', TemporaryFileStoreView.as_view(), name='temporary-file-store'),
    path('remove_file/', StoredFileRemoveView.as_view(), name='remove-stored-file'),
    path('view_file/<str:id>', StoredFileView.as_view(), name='stored-file-view'),

    path('public/', DocumentPublicList.as_view(), name='document-public-list'),
    path('public/<int:pk>', DocumentPublicDetail.as_view(), name='document-public-detail')
]