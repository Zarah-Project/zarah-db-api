import datetime

from django.shortcuts import get_object_or_404
from django_drf_filepond.api import store_upload, delete_stored_upload
from django_drf_filepond.models import TemporaryUpload, StoredUpload
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from document.models import Document
from document.serializers.serializers import DocumentWriteSerializer, DocumentReadFullSerializer, \
    DocumentListSerializer, DocumentReadIndividualSerializer
from document.serializers.serializers_public import DocumentReadPublicSerializer
from zarah_db_api.mixins.method_serializer_mixin import MethodSerializerMixin
from zarah_db_api.parsers import PlainTextParser


# Public views
from zarah_db_api.permissions import IsCreatorOrReadOnly


class DocumentPublicList(generics.ListAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentListSerializer
    authentication_classes = []
    permission_classes = []


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

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class DocumentDetail(MethodSerializerMixin, generics.RetrieveUpdateAPIView):
    queryset = Document.objects.all()
    permission_classes = [IsCreatorOrReadOnly]

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


class TemporaryFileStoreView(APIView):
    def post(self, request, format=None):
        temp_id = request.data.get('file', None)

        if temp_id:
            tu = TemporaryUpload.objects.get(upload_id=temp_id)
            su = store_upload(temp_id, "%s-%s" % (datetime.datetime.now().strftime("%Y%m%d_%H%M"), tu.upload_name))
            print(su.file.url)
            return Response(data={'file': su.file.url}, status=status.HTTP_200_OK)
        else:
            return Response(data='Not found', status=status.HTTP_404_NOT_FOUND)


class StoredFileRemoveView(APIView):
    parser_classes = (PlainTextParser, )

    def delete(self, request, format=None):
        file_id = request.data
        if file_id:
            try:
                delete_stored_upload(file_id, delete_file=True)
                return Response('OK', status=status.HTTP_200_OK)
            except StoredUpload.DoesNotExist:
                return Response(data='Not found', status=status.HTTP_404_NOT_FOUND)
