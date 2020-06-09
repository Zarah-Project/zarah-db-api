from django.conf import settings
from pysolr import SolrError
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from document.models import Document
from zarah_db_api.searchers import Searcher


class DocumentSearch(ListAPIView):
    """
    Returns a list of all the documents.
    """
    authentication_classes = tuple()
    permission_classes = tuple()
    queryset = Document.objects.all()
    core = getattr(settings, "SOLR_CORE", "zarah")

    def list(self, request, *args, **kwargs):
        limit = request.query_params.get('limit', 10)
        offset = request.query_params.get('offset', 0)

        filters = []
        filters_or = []
        date_filters = []

        qf = [
            'title_search^5',
            'zotero_search^2.5',
            'authority_search^2.5',
        ]
        params = {
            'search': request.query_params.get('query', ''),
            'ordering': request.query_params.get('ordering', '-score'),
            'qf': qf,
            'fl': 'id,title,created_by',
            'facet': True,
            'facet_fields': ['created_by_facet',],
            'facet_sort': 'index'
        }

        created = request.query_params.get('created', None)

        if created:
            filters.append({'created_by_facet': created})

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
