import pysolr
from django.conf import settings
from django.core.management import BaseCommand

from document.indexers.indexer import DocumentIndexer
from document.indexers.public_indexer import PublicIndexer
from document.models import Document


class Command(BaseCommand):
    help = 'Index documents.'

    def handle(self, *args, **options):
        solr_core = getattr(settings, "SOLR_CORE", "zarah-public")
        solr_url = "%s/%s" % (getattr(settings, "SOLR_URL", "http://localhost:8983/solr"), solr_core)
        solr = pysolr.Solr(solr_url)
        solr.delete(q='*:*')
        solr.commit()

        for document in Document.objects.all().iterator():
            indexer = PublicIndexer(document)
            indexer.index()
