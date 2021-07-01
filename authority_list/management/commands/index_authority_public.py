import pysolr
from django.conf import settings
from django.core.management import BaseCommand

from authority_list.indexers.public_authority_indexer import PublicAuthorityIndexer
from authority_list.models import Person, Organisation, Event, Place
from document.models import Document


class Command(BaseCommand):
    help = 'Index special records.'

    def handle(self, *args, **options):
        solr_core = getattr(settings, "SOLR_CORE", "zarah-public")
        solr_url = "%s/%s" % (getattr(settings, "SOLR_URL", "http://localhost:8983/solr"), solr_core)
        solr = pysolr.Solr(solr_url)

        solr.delete(q='id:person_*')
        solr.commit()
        for person in Person.objects.all().iterator():
            if Document.objects.filter(people__in=[person]).count() > 0:
                indexer = PublicAuthorityIndexer(person, 'person')
                indexer.index()

        solr.delete(q='id:organisation_*')
        solr.commit()
        for organisation in Organisation.objects.all().iterator():
            if Document.objects.filter(organisations__in=[organisation]).count() > 0:
                indexer = PublicAuthorityIndexer(organisation, 'organisation')
                indexer.index()

        solr.delete(q='id:event_*')
        solr.commit()
        for event in Event.objects.all().iterator():
            if Document.objects.filter(events__in=[event]).count() > 0:
                indexer = PublicAuthorityIndexer(event, 'event')
                indexer.index()

        solr.delete(q='id:place_*')
        solr.commit()
        for place in Place.objects.all().iterator():
            if Document.objects.filter(places__in=[place]).count() > 0:
                indexer = PublicAuthorityIndexer(place, 'place')
                indexer.index()