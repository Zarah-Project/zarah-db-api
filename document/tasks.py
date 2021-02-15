from document.indexers.public_indexer import PublicIndexer
from document.models import Document
from zarah_db_api.celery import app

from document.indexers.indexer import DocumentIndexer


@app.task
def index_document_admin(id):
    document = Document.objects.get(pk=id)
    indexer = DocumentIndexer(document)
    indexer.index()


@app.task
def index_document_public(id):
    document = Document.objects.get(pk=id)
    indexer = PublicIndexer(document)
    indexer.index()


@app.task
def remove_document_admin(id):
    document = Document.objects.get(pk=id)
    indexer = DocumentIndexer(document)
    indexer.remove_record()


@app.task
def remove_document_public(id):
    document = Document.objects.get(pk=id)
    indexer = PublicIndexer(document)
    indexer.remove_record()