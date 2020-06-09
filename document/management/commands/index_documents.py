from django.core.management import BaseCommand

from document.indexer import DocumentIndexer
from document.models import Document


class Command(BaseCommand):
    help = 'Index documents.'

    def handle(self, *args, **options):
        for document in Document.objects.all().iterator():
            indexer = DocumentIndexer(document)
            indexer.index()
