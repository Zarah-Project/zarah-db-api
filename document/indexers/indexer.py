import json
import os
from datetime import datetime

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
            'document_privacy': None,
            'metadata_privacy': None,

            # Search fields
            'title_search': [],
            'authority_search': [],
            'classification_search': [],
            'zotero_search': [],
            'full_text': [],

            # Facet fields
            'created_by_facet': None,

            # Sort fields
            'title_sort': None,
            'date_sort': None
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
        self.doc['created_by_sort'] = self.document.created_by.username if self.document.created_by else ''

        self.doc['metadata_privacy'] = self.document.record_type
        self.doc['document_privacy'] = self.document.attachment_type

        # Search
        self.doc['title_search'] = self.doc['title']

        for person in self.document.people.iterator():
            self.doc['authority_search'].append("%s %s" % (person.first_name, person.last_name))
            self.doc['authority_search'].append(person.notes if person.notes else "")
            for other_name in person.other_names.iterator():
                self.doc['authority_search'].append("%s %s" % (other_name.first_name, other_name.last_name))

        for organisation in self.document.organisations.iterator():
            self.doc['authority_search'].append(organisation.name)
            self.doc['authority_search'].append(organisation.acronym)
            self.doc['authority_search'].append(organisation.notes if organisation.notes else "")

        for place in self.document.places.iterator():
            self.doc['authority_search'].append(place.place_name)
            self.doc['authority_search'].append(place.notes if place.notes else "")
            for other_name in place.other_names.iterator():
                self.doc['authority_search'].append(other_name.place_name)

        for event in self.document.events.iterator():
            self.doc['authority_search'].append(event.event_full)

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
                self.doc['item_type'] = self._get_item_type(zotero_data['itemType'])

            # Zotero - Date
            if 'date' in zotero_data.keys():
                self.doc['year'] = zotero_data['date']
                self.doc['date_sort'] = self._parse_date(zotero_data['date'])

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

    def _get_item_type(self, item_type):
        zotero_item_types = getattr(settings, 'ZOTERO_ITEM_TYPES', {})
        if item_type in zotero_item_types:
            return zotero_item_types[item_type]
        else:
            return item_type

    def _parse_date(self, date):
        date = date.replace('Likely', '')
        date = date.replace('likely', '')
        date = date.replace('ca.', '')
        date = date.replace('[', '')
        date = date.replace('?]', '')
        date = date.replace('s', '')
        date = date.strip()

        try:
            datetime.strptime(date, "%Y")
            return "%s0000" % date
        except ValueError:
            pass

        try:
            d = datetime.strptime(date, "%B %Y")
            return "%s00" % (d.strftime("%Y%m"))
        except ValueError:
            pass

        try:
            d = datetime.strptime(date, "%d %B %Y")
            return "%d%02d%02d" % (d.year, d.month, d.day)
        except ValueError:
            pass

        if len(date) == 5 and date.endswith('s'):
            return "%s0000" % date[0:4]

        return ""
