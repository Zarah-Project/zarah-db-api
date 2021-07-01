from authority_list.models import Person, Organisation, Event, Place
from authority_list.indexers.public_authority_indexer import PublicAuthorityIndexer
from document.indexers.public_indexer import PublicIndexer
from document.models import Document
from zarah_db_api.celery import app

from document.indexers.indexer import DocumentIndexer


@app.task
def index_document_person(id):
    person = Person.objects.get(pk=id)
    documents = Document.objects.filter(people=person)
    for document in documents.iterator():
        indexer = DocumentIndexer(document)
        indexer.index()
        public_indexer = PublicIndexer(document)
        public_indexer.index()


@app.task
def index_document_organisation(id):
    organisation = Organisation.objects.get(pk=id)
    documents = Document.objects.filter(organisations=organisation)
    for document in documents.iterator():
        indexer = DocumentIndexer(document)
        indexer.index()
        public_indexer = PublicIndexer(document)
        public_indexer.index()


@app.task
def index_document_event(id):
    event = Event.objects.get(pk=id)
    documents = Document.objects.filter(events=event)
    for document in documents.iterator():
        indexer = DocumentIndexer(document)
        indexer.index()
        public_indexer = PublicIndexer(document)
        public_indexer.index()


@app.task
def index_document_place(id):
    place = Place.objects.get(pk=id)
    documents = Document.objects.filter(places=place)
    for document in documents.iterator():
        indexer = DocumentIndexer(document)
        indexer.index()
        public_indexer = PublicIndexer(document)
        public_indexer.index()


@app.task
def add_authority_record(id, type):
    if type == 'person':
        authority_record = Person.objects.get(pk=id)
    if type == 'organisation':
        authority_record = Organisation.objects.get(pk=id)
    if type == 'event':
        authority_record = Event.objects.get(pk=id)
    if type == 'place':
        authority_record = Place.objects.get(pk=id)
    indexer = PublicAuthorityIndexer(authority_record, type)
    indexer.index()


@app.task
def remove_authority_record(id, type):
    if type == 'person':
        authority_record = Person.objects.get(pk=id)
    if type == 'organisation':
        authority_record = Organisation.objects.get(pk=id)
    if type == 'event':
        authority_record = Event.objects.get(pk=id)
    if type == 'place':
        authority_record = Place.objects.get(pk=id)
    indexer = PublicAuthorityIndexer(authority_record, type)
    indexer.remove_record()
