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
    queryset = Document.objects.all()
    core = getattr(settings, "SOLR_CORE", "zarah")

    def list(self, request, *args, **kwargs):
        limit = request.query_params.get('limit', 10)
        offset = request.query_params.get('offset', 0)

        query = request.query_params.get('query', '')

        if query != '':
            ordering = request.query_params.get('ordering', '-score')
        else:
            ordering = request.query_params.get('ordering', 'title')

        # Title sort hack
        ordering = ordering.replace('title', 'title_sort')

        filters = []
        filters_or = []
        date_filters = []

        qf = [
            'title_search^5',
            'full_text^3',
            'zotero_search^2.5',
            'authority_search^2.5',
            'classification_search^2.5',
        ]
        params = {
            'search': query,
            'ordering': ordering,
            'qf': qf,
            'fl': 'id,title,language,item_type,year,created_by',
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
            user = self.request.user

            for doc in response.docs:
                if 'created_by' in doc.keys():
                    doc['is_editable'] = user.username == doc['created_by'] or user.is_staff or user.is_superuser
                else:
                    doc['is_editable'] = user.is_staff or user.is_superuser

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
