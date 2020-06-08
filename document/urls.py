from django.urls import path

from document.views import TemporaryFileStoreView, StoredFileRemoveView, DocumentList, DocumentDetail, \
    DocumentPublicList, DocumentPublicDetail

app_name = 'document'

urlpatterns = [
    path('', DocumentList.as_view(), name='document-list'),
    path('<int:pk>/', DocumentDetail.as_view(), name='document-detail'),

    path('store_file/', TemporaryFileStoreView.as_view(), name='temporary-file-store'),
    path('remove_file/', StoredFileRemoveView.as_view(), name='remove-stored-file'),

    path('public/', DocumentPublicList.as_view(), name='document-public-list'),
    path('public/<int:pk>', DocumentPublicDetail.as_view(), name='document-public-detail')
]