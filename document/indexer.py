import json
import os

import tika
from django_drf_filepond.api import get_stored_upload, get_stored_upload_file_data
from tika import parser

import pysolr
from django.conf import settings


class DocumentIndexer:
    """
    Class to index Document record records to Solr.
    """

    def __init__(self, document):
        self.document = document
        self.solr_core = getattr(settings, "SOLR_CORE", "zarah")
        self.solr_url = "%s/%s" % (getattr(settings, "SOLR_URL", "http://localhost:8983/solr"), self.solr_core)
        self.solr = pysolr.Solr(self.solr_url)
        self.doc = {
            # Display fields
            'id': None,
            'title': None,
            'created_by': None,

            # Search fields
            'title_search': [],
            'authority_search': [],
            'classification_search': [],
            'zotero_search': [],
            'full_text': [],

            # Facet fields
            'created_by_facet': None,

            # Sort fields
            'title_sort': None
        }

    def index(self):
        self._index_record()
        self._index_file_content()
        try:
            self.solr.add([self.doc], commit=True)
            print('Indexed record no. %s!' % self.doc['id'])
        except pysolr.SolrError as e:
            print('Error with record no. %s! Error: %s' % (self.doc['id'], e))

    def _index_record(self):
        self.doc['id'] = self.document.id
        self.doc['title'] = self.document.title
        self.doc['created_by'] = self.document.created_by.username if self.document.created_by else ''

        # Search
        self.doc['title_search'] = self.doc['title']

        for person in self.document.people.iterator():
            self.doc['authority_search'].append("%s %s" % (person.first_name, person.last_name))
            for other_name in person.other_names.iterator():
                self.doc['authority_search'].append("%s %s" % (other_name.first_name, other_name.last_name))

        for organisation in self.document.organisations.iterator():
            self.doc['authority_search'].append(organisation.name)
            self.doc['authority_search'].append(organisation.acronym)

        for place in self.document.places.iterator():
            self.doc['authority_search'].append(place.place_name)
            for other_name in place.other_names.iterator():
                self.doc['authority_search'].append(other_name.place_name)

        if self.document.zotero_data:
            zotero_data = json.loads(self.document.zotero_data)

            # Zotero - Creators
            if 'creators' in zotero_data.keys():
                for creator in zotero_data['creators']:
                    self.doc['zotero_search'].append(creator['firstName'])
                    self.doc['zotero_search'].append(creator['lastName'])

            # Zotero - Archive
            if 'archive' in zotero_data.keys():
                self.doc['zotero_search'].append(zotero_data['archive'])

        self.doc['full_text'].append(self.document.abstract)
        self.doc['full_text'].append(self.document.summary)

        # Classifications
        for keyword in self.document.triggering_factor_keywords.iterator():
            self.doc['classification_search'].append(keyword.keyword)

        for keyword in self.document.keywords.iterator():
            self.doc['classification_search'].append(keyword.keyword)

        for date in self.document.dates.iterator():
            self.doc['classification_search'].append(date.event)

        # Sort
        self.doc['title_sort'] = self.doc['title']

        self.doc['authority_search'] = ' '.join(self.doc['authority_search'])
        self.doc['zotero_search'] = ' '.join(self.doc['zotero_search'])

    def _index_file_content(self):
        tika.TikaClientOnly = True
        for file in self.document.files.iterator():
            if file.file_id:
                try:
                    su = get_stored_upload(file.file_id)
                    (filename, bytes_io) = get_stored_upload_file_data(su)
                    parsed = parser.from_file(os.path.join(settings.DJANGO_DRF_FILEPOND_FILE_STORE_PATH, filename))
                    self.doc['full_text'].append(parsed["content"])
                except Exception as e:
                    print(e)
