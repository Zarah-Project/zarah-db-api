import json
import os
import pysolr
import tika

from datetime import datetime
from metadata.models import Classification

from django_drf_filepond.api import get_stored_upload, get_stored_upload_file_data
from tika import parser

from django.conf import settings

tika.TikaClientOnly = True


class PublicIndexer:
    """
    Class to index Document records to Solr public.
    """

    def __init__(self, document):
        self.document = document
        self.solr_core = getattr(settings, "SOLR_PUBLIC_CORE", "zarah-public")
        self.solr_url = "%s/%s" % (getattr(settings, "SOLR_URL", "http://localhost:8983/solr"), self.solr_core)
        self.solr = pysolr.Solr(self.solr_url)
        self.doc = {
            # Display fields
            'id': None,
            'title': None,
            'item_type': None,
            'attachment_type': None,
            'author': None,
            'archive': None,
            'archive_location': None,
            'date': None,
            'file': [],

            # Search fields
            'title_search': None,
            'abstract_search': None,
            'attachment_text_search': None,
            'keyword_search': [],
            'classification_search': [],
            'authority_search': [],
            'zotero_search': [],
            'date_search': "",

            # Facet fields
            'person_facet': [],
            'person_id_facet': [],
            'organisation_facet': [],
            'organisation_id_facet': [],
            'place_facet': [],
            'place_id_facet': [],
            'event_facet': [],
            'event_id_facet': [],
            'keyword_facet': [],
            'historical_context_facet': [],
            'labour_conditions_facet': [],
            'living_conditions_facet': [],
            'labour_relations_facet': [],
            'agendas_facet': [],
            'activist_repertoire_facet': [],
            'activist_repertoire_scale_facet': [],
            'format_of_participation_facet': [],
            'knowledge_production_facet': [],
            'date_facet': [],
            'archive_facet': [],
            'language_facet': [],
            'item_type_facet': [],
            'author_facet': [],

            # Sort fields
            'title_sort': None,
            'date_sort': None
        }

    def index(self):
        self._index_record()
        if self.document.attachment_type == 'default':
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
        # Stored fields
        self.doc['id'] = self.document.id
        self.doc['title'] = self.document.title
        self.doc['item_type'] = self.document.item_type
        self.doc['attachment_type'] = self.document.attachment_type

        # Facets
        self.doc['item_type_facet'] = self.document.item_type

        # Search
        self.doc['title_search'] = self.doc['title']

        if self.document.record_type == 'default':
            self.doc['abstract_search'] = self.document.abstract

            # Authority Records
            for person in self.document.people.iterator():
                if person.is_public:
                    self.doc['authority_search'].append("%s %s" % (person.first_name, person.last_name))
                    self.doc['authority_search'].append(person.notes if person.notes else "")
                    self.doc['person_facet'].append("%s" % person.full_name)
                    self.doc['person_id_facet'].append("%s#%s" % (person.full_name, person.id))
                    for other_name in person.other_names.iterator():
                        self.doc['authority_search'].append("%s %s" % (other_name.first_name, other_name.last_name))

            for organisation in self.document.organisations.iterator():
                if organisation.is_public:
                    self.doc['authority_search'].append(organisation.name)
                    self.doc['authority_search'].append(organisation.acronym)
                    self.doc['authority_search'].append(organisation.notes if organisation.notes else "")
                    self.doc['organisation_facet'].append("%s" % organisation.full_name)
                    self.doc['organisation_id_facet'].append("%s#%s" % (organisation.full_name, organisation.id))

            for place in self.document.places.iterator():
                if place.is_public:
                    self.doc['authority_search'].append(place.place_full)
                    self.doc['authority_search'].append(place.notes if place.notes else "")
                    self.doc['place_facet'].append(place.place_full)
                    self.doc['place_id_facet'].append("%s#%s" % (place.place_full, place.id))

                    for other_name in place.other_names.iterator():
                        self.doc['authority_search'].append(other_name.place_name)

            for event in self.document.events.iterator():
                if event.is_public:
                    self.doc['authority_search'].append(event.event_full)
                    self.doc['event_facet'].append(event.event_full)
                    self.doc['event_id_facet'].append("%s#%s" % (event.event_full, event.id))

        # Zotero
        if self.document.zotero_data:
            zotero_data = json.loads(self.document.zotero_data)

            # Zotero - Creators
            if 'creators' in zotero_data.keys():
                for creator in zotero_data['creators']:
                    first_name = ""
                    last_name = ""
                    if 'firstName' in creator.keys():
                        first_name = creator['firstName']
                    if 'lastName' in creator.keys():
                        last_name = creator['lastName']
                    self.doc['zotero_search'].append(("%s %s" % (first_name, last_name)).strip())
                    self.doc['author'] = ("%s %s" % (first_name, last_name)).strip()
                    self.doc['author_facet'] = ("%s %s" % (first_name, last_name)).strip()

            if 'language' in zotero_data.keys():
                if zotero_data['language'] != '':
                    languages = zotero_data['language'].split(',')
                    for idx, lang in enumerate(languages):
                        if lang.strip() == 'English':
                            if len(languages) == 1 or idx == 0:
                                self.doc['language_facet'].append(lang.strip())
                        else:
                            self.doc['language_facet'].append(lang.strip())

            # Zotero - Archive
            if 'archive' in zotero_data.keys():
                self.doc['zotero_search'].append(zotero_data['archive'])
                self.doc['archive'] = zotero_data['archive']
                self.doc['archive_facet'] = zotero_data['archive']

            # Zotero - Archive Location
            if 'archiveLocation' in zotero_data.keys():
                self.doc['zotero_search'].append(zotero_data['archiveLocation'])
                self.doc['archive_location'] = zotero_data['archiveLocation']

            # Zotero - Date
            if 'date' in zotero_data.keys():
                self.doc['date'] = zotero_data['date']
                self.doc['date_sort'] = self._parse_date(zotero_data['date'])

            # Date facets
                date = zotero_data['date']
                dates = self._from_to_date(date)

                if dates[0] != 0 and dates[1] != 0:
                    self.doc['date_search'] = "[%s TO %s]" % (dates[0], dates[1])
                    for year in range(int(dates[0]), int(dates[1])):
                        self.doc['date_facet'].append(year)

        # Keywords
        if self.document.record_type == 'default':
            for keyword in self.document.triggering_factor_keywords.iterator():
                self.doc['keyword_search'].append(keyword.keyword)
                self.doc['keyword_facet'].append(keyword.keyword)

            for keyword in self.document.keywords.iterator():
                self.doc['keyword_search'].append(keyword.keyword)
                self.doc['keyword_facet'].append(keyword.keyword)

        # Classifications
        if self.document.record_type != 'individual':
            self.doc['historical_context_facet'] = self._index_classification('historical_context')

        if self.document.record_type == 'default':
            self.doc['labour_conditions_facet'] = self._index_classification('labour_conditions')
            self.doc['living_conditions_facet'] = self._index_classification('living_conditions')
            self.doc['labour_relations_facet'] = self._index_classification('labour_relations')
            self.doc['agendas_facet'] = self._index_classification('agendas')
            self.doc['activist_repertoire_facet'] = self._index_classification('activist_repertoire')
            self.doc['activist_repertoire_scale_facet'] = self._index_classification('activist_repertoire_scale')
            self.doc['format_of_participation_facet'] = self._index_classification('format_of_participation')
            self.doc['knowledge_production_facet'] = self._index_classification('knowledge_production')

        # Sort
        self.doc['title_sort'] = self.doc['title']

    def _index_classification(self, field):
        values = []
        classifications = Classification.objects.filter(
            document=self.document, classification_field__category__key=field
        )
        for classification in classifications:
            if classification.classification_field.field_type == 'tag':
                values.append(classification.classification_field.full_name)

                cs = classification.classification_field.full_name.split('->')
                for c in cs:
                    self.doc['classification_search'].append(c.strip())

        return values

    def _index_file_content(self):
        for file in self.document.files.iterator():
            if file.file_id:
                try:
                    su = get_stored_upload(file.file_id)
                    (filename, bytes_io) = get_stored_upload_file_data(su)
                    parsed = parser.from_file(os.path.join(settings.DJANGO_DRF_FILEPOND_FILE_STORE_PATH, filename))
                    self.doc['attachment_text_search'] = parsed["content"]
                except Exception as e:
                    print(e)

    def _from_to_date(self, date):
        if date.find('Likely') > -1:
            d = self._parse_date(date)
            if self._parse_date(date) != "":
                return [int(d[0:4]), int(d[0:4])+1]

        if date.find('likely') > -1:
            d = self._parse_date(date)
            if self._parse_date(date) != "":
                return [int(d[0:4]), int(d[0:4])+1]

        if date.find('ca.') > -1:
            d = self._parse_date(date)
            if self._parse_date(date) != "":
                return [int(d[0:4])-1, int(d[0:4])+1]

        if date.startswith('['):
            d = self._parse_date(date)
            if self._parse_date(date) != "":
                return [int(d[0:4])-1, int(d[0:4])+1]

        if date.endswith('s'):
            d = self._parse_date(date)
            if self._parse_date(date) != "":
                return ["%s0" % d[0:3], "%s9" % d[0:3]]

        d = self._parse_date(date)
        if self._parse_date(date) != "":
            return [int(d[0:4]), int(d[0:4]) + 1]
        else:
            return [0, 0]

    def _parse_date(self, date):
        date = date.replace('Likely', '')
        date = date.replace('likely', '')
        date = date.replace('ca.', '')
        date = date.replace('[', '')
        date = date.replace('?', '')
        date = date.replace(']', '')
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
