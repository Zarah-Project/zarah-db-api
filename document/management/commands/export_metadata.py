import json

from django.core.management import BaseCommand
from document.models import Document

from document.serializers.serializers_export import DocumentExportSerializer


class Command(BaseCommand):
    help = 'Exporting metadata of documents.'

    def handle(self, *args, **options):
        documents = []
        for document in Document.objects.all():
            serializer = DocumentExportSerializer(document)
            documents.append(serializer.data)
        with open('dataset.json', 'w') as json_file:
            json.dump(documents, json_file, indent=4)
        print("Finished!")
