import json
import os

import tika
tika.TikaClientOnly = True

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
            'item_type': None,
            'language': None,
            'year': None,

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

    def remove_record(self):
        self.solr.delete(self.document.id)
        self.solr.commit()

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

        for event in self.document.events.iterator():
            self.doc['authority_search'].append(event.event)

        if self.document.zotero_data:
            zotero_data = json.loads(self.document.zotero_data)

            # Zotero - Creators
            if 'creators' in zotero_data.keys():
                for creator in zotero_data['creators']:
                    if 'firstName' in creator.keys():
                        self.doc['zotero_search'].append(creator['firstName'])
                    if 'lastName' in creator.keys():
                        self.doc['zotero_search'].append(creator['lastName'])

            # Zotero - Archive
            if 'archive' in zotero_data.keys():
                self.doc['zotero_search'].append(zotero_data['archive'])

            # Zotero - Archive Location
            if 'archiveLocation' in zotero_data.keys():
                self.doc['zotero_search'].append(zotero_data['archiveLocation'])

            # Zotero - Language
            if 'language' in zotero_data.keys():
                self.doc['language'] = zotero_data['language']

            # Zotero - Item Type
            if 'itemType' in zotero_data.keys():
                self.doc['item_type'] = zotero_data['itemType']

            # Zotero - Item Type
            if 'date' in zotero_data.keys():
                self.doc['year'] = zotero_data['date']

        self.doc['full_text'].append(self.document.abstract)
        self.doc['full_text'].append(self.document.summary)

        # Classifications
        for keyword in self.document.triggering_factor_keywords.iterator():
            self.doc['classification_search'].append(keyword.keyword)

        for keyword in self.document.keywords.iterator():
            self.doc['classification_search'].append(keyword.keyword)

        for explanation in self.document.explanations.iterator():
            self.doc['full_text'].append(explanation.explanation)

        # Sort
        self.doc['title_sort'] = self.doc['title']

        self.doc['authority_search'] = ' '.join(self.doc['authority_search'])
        self.doc['zotero_search'] = ' '.join(self.doc['zotero_search'])

    def _index_file_content(self):
        for file in self.document.files.iterator():
            if file.file_id:
                try:
                    su = get_stored_upload(file.file_id)
                    (filename, bytes_io) = get_stored_upload_file_data(su)
                    parsed = parser.from_file(os.path.join(settings.DJANGO_DRF_FILEPOND_FILE_STORE_PATH, filename))
                    self.doc['full_text'].append(parsed["content"])
                except Exception as e:
                    print(e)
