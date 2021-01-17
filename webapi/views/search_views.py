from django.conf import settings
from pysolr import SolrError
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from document.models import Document
from zarah_db_api.searchers import Searcher


class DocumentPublicSearch(ListAPIView):
    """
    Returns a list of all the documents.
    """
    queryset = Document.objects.all()
    core = getattr(settings, "SOLR_CORE", "zarah-public")
    authentication_classes = []
    permission_classes = []

    def list(self, request, *args, **kwargs):
        limit = request.query_params.get('limit', 10)
        if limit == '':
            limit = 10
        offset = request.query_params.get('offset', 0)

        query = request.query_params.get('query', '')

        if query != '':
            ordering = request.query_params.get('ordering', '-score')
        else:
            ordering = request.query_params.get('ordering', 'title')

        filters = []
        filters_or = []
        date_filters = []

        qf = []
        self._append_query_fields(request, qf)

        params = {
            'search': query,
            'ordering': ordering,
            'qf': qf,
            'fl': 'id,title,item_type,attachment_type,author,archive,archive_location,date',
            'facet': True,
            'facet_fields': [
                'person_facet', 'organisation_facet', 'place_facet', 'event_facet', 'keyword_facet',
                'historical_context_facet', 'labour_conditions_facet', 'living_conditions_facet',
                'labour_relations_facet', 'activist_repertoire_facet', 'activist_repertoire_scale_facet',
                'format_of_participation_facet', 'knowledge_production_facet'
            ],
            'facet_sort': 'index'
        }

        filters = self._append_filters(request, filters, 'person')
        filters = self._append_filters(request, filters, 'organisation')
        filters = self._append_filters(request, filters, 'place')
        filters = self._append_filters(request, filters, 'event')
        filters = self._append_filters(request, filters, 'keyword')
        filters = self._append_filters(request, filters, 'historical_context')
        filters = self._append_filters(request, filters, 'labour_conditions')
        filters = self._append_filters(request, filters, 'living_conditions')
        filters = self._append_filters(request, filters, 'labour_relations')
        filters = self._append_filters(request, filters, 'activist_repertoire')
        filters = self._append_filters(request, filters, 'activist_repertoire_scale')
        filters = self._append_filters(request, filters, 'format_of_participation')
        filters = self._append_filters(request, filters, 'knowledge_production')

        params['filters'] = filters
        params['filters_or'] = filters_or
        params['date_filters'] = date_filters

        searcher = Searcher(self.core)
        searcher.initialize(params, start=offset, rows_per_page=limit, tie_breaker='title_sort asc')

        try:
            response = searcher.search()
        except SolrError as e:
            return Response(status=HTTP_400_BAD_REQUEST, data={'error': str(e)})

        resp = {
            'count': response.hits,
            'results': response.docs,
            'facets': response.facets
        }
        if (int(limit) + int(offset)) < int(response.hits):
            resp['next'] = True
        return Response(resp)

    def _append_query_fields(self, request, qf):
        fields = {
            'attachment_text': 'attachment_text_search^5',
            'title': 'title_search^3',
            'abstract': 'abstract_search^2.5',
            'authority': 'authority_search^2.5',
            'zotero': 'zotero_search^1.5',
            'keyword': 'keyword_search^1.5'
        }
        qf_param = request.query_params.getlist('query_fields', None)
        if len(qf_param) > 0:
            for qfp in qf_param:
                if qfp in fields:
                    qf.append(fields[qfp])

        qf_param = request.query_params.getlist('query_fields[]', None)
        if len(qf_param) > 0:
            for qfp in qf_param:
                if qfp in fields:
                    qf.append(fields[qfp])

        if len(qf) == 0:
            for key in fields.keys():
                qf.append(fields[key])

        return qf

    def _append_filters(self, request, filters, field):
        f_param = request.query_params.getlist('%s' % field, None)
        if len(f_param) > 0:
            for fp in f_param:
                filters.append({'%s_facet' % field: fp})

        f_param = request.query_params.getlist('%s[]' % field, None)
        if len(f_param) > 0:
            for fp in f_param:
                filters.append({'%s_facet' % field: fp})

        return filters