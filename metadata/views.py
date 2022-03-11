from django.conf import settings
from rest_framework import generics, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView
from pyzotero import zotero

from metadata.models import ClassificationField, ConsentType
from metadata.serializers import ClassificationFieldListSerializer, ConsentFieldsListSerializer


class ClassificationFieldsList(generics.ListAPIView):
    serializer_class = ClassificationFieldListSerializer
    queryset = ClassificationField.objects.filter(parent__isnull=True)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category__key',)
    pagination_class = None


class ConsentFieldsList(generics.ListAPIView):
    serializer_class = ConsentFieldsListSerializer
    queryset = ConsentType.objects.all()
    pagination_class = None


class ZoteroSearch(APIView):
    def get(self, request, format=None):
        items = []
        search = request.query_params.get('search', None)

        if search:
            zot = zotero.Zotero(settings.ZOTERO_LIBRARY_ID, 'group', settings.ZOTERO_API_KEY)
            items = zot.items(q=search, qmode='everything')
            for item in items:
                if 'itemType' in item:
                    item['itemType'] = self._get_item_type(item['itemType'])
        return Response(items, status=status.HTTP_200_OK)

    def _get_item_type(self, item_type):
        zotero_item_types = settings.get('ZOTERO_ITEM_TYPES', {})
        if item_type in zotero_item_types:
            return zotero_item_types[item_type]
