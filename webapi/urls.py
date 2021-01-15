from django.urls import path

from webapi.views import DocumentPublicDetail

app_name = 'webapi'

urlpatterns = [
    path('document/<int:pk>/', DocumentPublicDetail.as_view(), name='document-detail'),
]