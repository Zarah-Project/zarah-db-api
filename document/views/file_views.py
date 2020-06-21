import datetime

from django.core.exceptions import ObjectDoesNotExist
from django_drf_filepond.api import store_upload, delete_stored_upload, get_stored_upload, get_stored_upload_file_data
from django_drf_filepond.models import TemporaryUpload, StoredUpload

from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from document.models import DocumentFile
from zarah_db_api.parsers import PlainTextParser


class TemporaryFileStoreView(APIView):
    def post(self, request, format=None):
        temp_id = request.data.get('file', None)

        if temp_id:
            tu = TemporaryUpload.objects.get(upload_id=temp_id)
            su = store_upload(temp_id, "%s-%s" % (datetime.datetime.now().strftime("%Y%m%d_%H%M"), tu.upload_name))
            return Response(data={'file_id': su.upload_id}, status=status.HTTP_200_OK)
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


class StoredFileView(APIView):
    def get(self, request, id):
        restricted = False

        try:
            document_file = DocumentFile.objects.get(file_id=id)
            attachmemnt_type = document_file.document.attachment_type

            if attachmemnt_type == 'individual':
                if not request.user.is_staff or \
                        not request.user.is_superuser or request.user != document_file.document.created_by:
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
                response["Content-Disposition"] = "attachment; filename={0}".format(filename)
                response["Content-Type"] = 'application/pdf'
                return response
            except FileNotFoundError:
                return Response(data='Not found', status=status.HTTP_404_NOT_FOUND)
