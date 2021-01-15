from rest_framework import generics
from rest_framework.generics import get_object_or_404

from document.models import Document
from webapi.serializers import DocumentReadPublicSerializer, DocumentReadTeamSerializer, DocumentReadIndividualSerializer


class DocumentPublicDetail(generics.RetrieveAPIView):
    queryset = Document.objects.all()
    authentication_classes = []
    permission_classes = []

    def get_serializer_class(self):
        document = get_object_or_404(Document, pk=self.kwargs.get('pk', None))
        if document.record_type == 'default':
            return DocumentReadPublicSerializer
        if document.record_type == 'team':
            return DocumentReadTeamSerializer
        if document.record_type == 'individual':
            return DocumentReadIndividualSerializer
