from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from document.indexer import DocumentIndexer
from document.models import Document
from document.serializers.serializers import DocumentWriteSerializer, DocumentReadFullSerializer, \
    DocumentListSerializer, DocumentReadIndividualSerializer
from document.serializers.serializers_public import DocumentReadPublicSerializer
from zarah_db_api.mixins.method_serializer_mixin import MethodSerializerMixin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


# Public views
from zarah_db_api.permissions import IsCreatorOrReadOnly


class DocumentPublicList(generics.ListAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentListSerializer
    authentication_classes = []
    permission_classes = []
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['people', 'places', 'organisations']
    ordering_fields = ['title']


class DocumentPublicDetail(generics.RetrieveAPIView):
    queryset = Document.objects.all()
    authentication_classes = []
    permission_classes = []

    def get_serializer_class(self):
        return DocumentReadPublicSerializer


# Team and Admin views
class DocumentList(MethodSerializerMixin, generics.ListCreateAPIView):
    queryset = Document.objects.all()
    method_serializer_classes = {
        ('GET', ): DocumentListSerializer,
        ('PUT', 'POST', 'PATCH', 'DELETE'): DocumentWriteSerializer
    }
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['people', 'places', 'organisations', 'events']
    ordering_fields = ['title']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class DocumentClone(APIView):
    def post(self, request, *args, **kwargs):
        document_id = self.kwargs.get('pk', None)
        document = get_object_or_404(Document, pk=document_id)
        clone = document.make_clone()

        clone.title = '[COPY] ' + clone.title
        clone.created_by = self.request.user

        clone.save()
        return Response(status=status.HTTP_200_OK)


class DocumentDetail(MethodSerializerMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    permission_classes = [IsCreatorOrReadOnly]

    def perform_destroy(self, instance):
        indexer = DocumentIndexer(instance)
        indexer.remove_record()
        instance.delete()

    def get_serializer_class(self):
        method = self.request._request.method

        user = self.request.user
        document = get_object_or_404(Document, pk=self.kwargs.get('pk', None))

        if method == 'GET':
            if document.created_by:
                # Own record
                if document.created_by.id == user.id:
                    return DocumentReadFullSerializer
                # Default
                elif document.record_type == 'default':
                    return DocumentReadFullSerializer
                # Team
                elif document.record_type == 'team':
                    return DocumentReadFullSerializer
                # Individual
                else:
                    return DocumentReadIndividualSerializer
            else:
                return DocumentReadFullSerializer
        else:
            return DocumentWriteSerializer
