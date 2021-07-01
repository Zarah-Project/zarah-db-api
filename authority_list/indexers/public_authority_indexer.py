import pysolr
from django.conf import settings


class PublicAuthorityIndexer:
    """
        Class to index Document records to Solr public.
        """

    def __init__(self, authority_record, record_type):
        self.authority_record = authority_record
        self.record_type = record_type
        self.solr_core = getattr(settings, "SOLR_PUBLIC_CORE", "zarah-public")
        self.solr_url = "%s/%s" % (getattr(settings, "SOLR_URL", "http://localhost:8983/solr"), self.solr_core)
        self.solr = pysolr.Solr(self.solr_url)
        self.doc = {
            # Display fields
            'id': None,
            'title': None,
            'record_type': None,

            # Search fields
            'name_search': [],
            'note_search': "",
            'date_search': "",

            # Sort fields
            'title_sort': None,
        }

    def index(self):
        if self.authority_record.is_public:
            self._index_record()
        else:
            self.remove_record()
        try:
            self.solr.add([self.doc], commit=True)
            print('Indexed authority record no. %s!' % self.doc['id'])
        except pysolr.SolrError as e:
            print('Error with record no. %s! Error: %s' % (self.doc['id'], e))

    def _index_record(self):
        # Stored fields
        self.doc['id'] = "%s_%s" % (self.record_type, self.authority_record.id)
        self._index_name()
        self.doc['record_type'] = self.record_type
        if hasattr(self.authority_record, 'notes'):
            self.doc['note_search'] = self.authority_record.notes

    def _index_name(self):
        if self.record_type == 'person':
            self.doc['name'] = self.authority_record.full_name
            self.doc['name_search'].append(self.authority_record.full_name)
            for other_name in self.authority_record.other_names.iterator():
                self.doc['name_search'].append("%s %s" % (other_name.first_name, other_name.last_name))
        if self.record_type == 'organisation':
            self.doc['name'] = self.authority_record.full_name
            self.doc['name_search'] = self.authority_record.full_name
        if self.record_type == 'place':
            self.doc['name'] = self.authority_record.place_full
            self.doc['name_search'].append(self.authority_record.place_full)
            for other_name in self.authority_record.other_names.iterator():
                self.doc['name_search'].append(other_name.place_name)
        if self.record_type == 'event':
            self.doc['name'] = self.authority_record.event_full
            self.doc['name_search'] = self.authority_record.event_full

    def remove_record(self):
        self.solr.delete("%s_%s" % (self.record_type, self.authority_record.id))
        self.solr.commit()
