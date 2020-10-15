import pysolr
from django.conf import settings
from django.core.management import BaseCommand

from document.indexer import DocumentIndexer
from document.models import Document


class Command(BaseCommand):
    help = 'Index documents.'

    def handle(self, *args, **options):
        solr_core = getattr(settings, "SOLR_CORE", "zarah")
        solr_url = "%s/%s" % (getattr(settings, "SOLR_URL", "http://localhost:8983/solr"), solr_core)
        solr = pysolr.Solr(solr_url)
        solr.delete(q='*:*')
        solr.commit()

        for document in Document.objects.all().iterator():
            indexer = DocumentIndexer(document)
            indexer.index()
