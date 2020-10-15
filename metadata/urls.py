from django.urls import path
from metadata.views import ClassificationFieldsList, ZoteroSearch, ConsentFieldsList

app_name = 'metadata'

urlpatterns = [
    path('classifications/', ClassificationFieldsList.as_view(), name='classification-field-list'),
    path('consents/', ConsentFieldsList.as_view(), name='consent-field-list'),
    path('zotero/', ZoteroSearch.as_view(), name='zotero-list')
]