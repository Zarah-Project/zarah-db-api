from django.urls import path

from webapi.views import DocumentPublicDetail, StoredFilePublicView

app_name = 'webapi'

urlpatterns = [
    path('document/<int:pk>/', DocumentPublicDetail.as_view(), name='document-detail'),

    path('view_file/<str:id>', StoredFilePublicView.as_view(), name='stored-file-pubic-view'),
]