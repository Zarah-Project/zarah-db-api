from celery import shared_task

from document.indexers.indexer import DocumentIndexer
from document.models import Document


@shared_task
def hello():
    print("Hello there!")


@shared_task
def index_document(document_id):
    document = Document.objects.get(pk=document_id)
    indexer = DocumentIndexer(document)
    indexer.index()
