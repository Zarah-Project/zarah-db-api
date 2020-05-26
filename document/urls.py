from django.urls import path

from document.views import TemporaryFileStoreView, StoredFileRemoveView, DocumentList, DocumentDetail

app_name = 'document'

urlpatterns = [
    path('', DocumentList.as_view(), name='document-list'),
    path('<int:pk>/', DocumentDetail.as_view(), name='document-list'),
    path('store_file/', TemporaryFileStoreView.as_view(), name='temporary-file-store'),
    path('remove_file/', StoredFileRemoveView.as_view(), name='remove-stored-file')
]