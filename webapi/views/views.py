from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Prefetch
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt
from django_drf_filepond.api import get_stored_upload, get_stored_upload_file_data
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from authority_list.models import Person, Organisation, Place, Event
from document.models import Document, DocumentFile
from webapi.serializers import DocumentReadPublicSerializer, DocumentReadTeamSerializer, \
    DocumentReadIndividualSerializer, DocumentCitationSerializer


class DocumentPublicDetail(generics.RetrieveAPIView):
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

    def get_queryset(self):
        return Document.objects.prefetch_related(
            Prefetch('people', queryset=Person.objects.filter(is_public=True)),
            Prefetch('organisations', queryset=Organisation.objects.filter(is_public=True)),
            Prefetch('places', queryset=Place.objects.filter(is_public=True)),
            Prefetch('events', queryset=Event.objects.filter(is_public=True))
        )


class DocumentCitation(generics.RetrieveAPIView):
    queryset = Document.objects.all()
    authentication_classes = []
    permission_classes = []
    serializer_class = DocumentCitationSerializer


class StoredFilePublicView(APIView):
    authentication_classes = []
    permission_classes = []

    @method_decorator(xframe_options_exempt)
    def get(self, request, id):
        restricted = False

        try:
            document_file = DocumentFile.objects.get(file_id=id)
            attachmemnt_type = document_file.document.attachment_type

            if attachmemnt_type != 'default':
                restricted = True
        except ObjectDoesNotExist:
            restricted = False

        if restricted:
            return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            try:
                su = get_stored_upload(id)
                (filename, bytes_io) = get_stored_upload_file_data(su)
                response = Response()
                response.content = bytes_io
                response["Content-Disposition"] = "inline; filename={0}".format(filename)
                response["Content-Type"] = 'application/pdf'
                return response
            except FileNotFoundError:
                return Response(data='Not found', status=status.HTTP_404_NOT_FOUND)