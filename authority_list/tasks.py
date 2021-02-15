from authority_list.models import Person, Organisation, Event, Place
from document.indexers.public_indexer import PublicIndexer
from document.models import Document
from zarah_db_api.celery import app

from document.indexers.indexer import DocumentIndexer


@app.task
def index_person(id):
    person = Person.objects.get(pk=id)
    documents = Document.objects.filter(people=person)
    for document in documents.iterator():
        indexer = DocumentIndexer(document)
        indexer.index()
        public_indexer = PublicIndexer(document)
        public_indexer.index()


@app.task
def index_organisation(id):
    organisation = Organisation.objects.get(pk=id)
    documents = Document.objects.filter(organsations=organisation)
    for document in documents.iterator():
        indexer = DocumentIndexer(document)
        indexer.index()
        public_indexer = PublicIndexer(document)
        public_indexer.index()


@app.task
def index_event(id):
    event = Event.objects.get(pk=id)
    documents = Document.objects.filter(events=event)
    for document in documents.iterator():
        indexer = DocumentIndexer(document)
        indexer.index()
        public_indexer = PublicIndexer(document)
        public_indexer.index()


@app.task
def index_place(id):
    place = Place.objects.get(pk=id)
    documents = Document.objects.filter(places=place)
    for document in documents.iterator():
        indexer = DocumentIndexer(document)
        indexer.index()
        public_indexer = PublicIndexer(document)
        public_indexer.index()
