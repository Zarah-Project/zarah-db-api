import locale

import pysolr
from django.conf import settings


class Searcher:
    """
    Class to search records from Solr.
    """

    def __init__(self, solr_core):
        self.solr_url = "%s/%s" % (getattr(settings, "SOLR_URL", "http://localhost:8983/solr"), solr_core)
        self.solr = pysolr.Solr(self.solr_url)
        self.q = {}
        self.fq = []
        self.sort = ""
        self.qf = ""
        self.fl = ""
        self.hl = ""
        self.hl_fl = ""
        self.start = 0
        self.rows_per_page = 10
        self.tie_breaker = ""
        self.paginated = True
        self.facet = False
        self.facet_fields = []
        self.facet_sort = 'count'

    def initialize(self, params, start=0, rows_per_page=10, tie_breaker="", paginated=True):
        self.start = start
        self.rows_per_page = rows_per_page
        self.tie_breaker = tie_breaker
        self.paginated = paginated

        search = params.get('search', '*:*')
        self.set_q(search)

        filters = params.get('filters', [])
        self.set_fq(filters, ' AND ')

        filters_or = params.get('filters_or', "")
        self.set_fq(filters_or, ' OR ')

        date_filters = params.get('date_filters', [])
        self.set_date_fq(date_filters)

        ordering = params.get('ordering', "")
        self.set_order(ordering)

        qf = params.get('qf', '')
        self.set_qf(qf)

        fl = params.get('fl', '')
        self.set_fl(fl)

        hl = params.get('hl', None)
        if hl:
            self.hl = hl
        else:
            self.hl = "false"

        hl_fl = params.get('hl.fl', None)
        if hl_fl:
            self.hl_fl = hl_fl

        # Set faceting
        facet = params.get('facet', False)
        if facet:
            self.facet = "on"
        else:
            self.facet = "false"
        self.facet_fields = params.get('facet_fields', [])
        self.facet_sort = params.get('facet_sort', 'count')

    def search(self, cursor_mark=''):
        search_kwargs = {
            'defType': 'edismax',
            'qf': self.qf,
            'fq': self.fq,
            'fl': self.fl,
            'q.op': 'AND',
            'hl': self.hl,
            'hl.fl': self.hl_fl,
            'facet.field': self.facet_fields,
            'facet.sort': self.facet_sort,
            'facet.limit': -1,
            'facet.mincount': 1
        }
        if self.paginated:
            results = self.solr.search(
                q=self.q,
                sort=self.sort,
                start=self.start,
                rows=self.rows_per_page,
                facet=self.facet,
                **search_kwargs
            )
        else:
            results = self.solr.search(
                q=self.q,
                sort=self.sort,
                facet=self.facet,
                cursorMark=cursor_mark,
                **search_kwargs
            )
        return self.reorder_facets(results)

    def set_q(self, search):
        self.q = search
        if search == "":
            self.q = "*:*"

    def set_fq(self, filters, logic=' AND '):
        fq_filters = []
        for f in filters:
            for k, v in f.items():
                fq_filters.append('%s:"%s"' % (k, v))
        self.fq.append(logic.join(fq_filters))

    def set_date_fq(self, date_filters):
        for f in date_filters:
            for k, v in f.items():
                self.fq.append('%s:%s' % (k, v))

    def get_tie_breaker(self, ordering):
        # Tie breaker
        if ordering == 'score':
            if len(self.tie_breaker) > 0:
                return '%s,id asc' % self.tie_breaker
            else:
                return 'id asc'
        else:
            return 'score desc,id asc'

    def set_order(self, ordering):
        # Ordering params
        order_list = []
        ordering = ordering.split(',')

        for order in ordering:
            ordering_direction = 'asc'
            if order == '':
                order = '-score'

            if order[0] == '-':
                order = order[1:]
                ordering_direction = 'desc'
            order_list.append("%s %s" % (order, ordering_direction))

        tie_breaker = self.get_tie_breaker(ordering)
        self.sort = "%s,%s" % (",".join(order_list), tie_breaker)

    def set_qf(self, qf):
        self.qf = " ".join(qf)

    def set_fl(self, fl):
        self.fl = fl

    def reorder_facets(self, results):
        keys_to_check = ['person_facet', 'organisation_facet', 'place_facet', 'event_facet', 'author_facet']
        for key in results.facets['facet_fields'].keys():
            if key in keys_to_check:
                records_dict = {}
                record_values = []
                result_values = []
                records = results.facets['facet_fields'][key]
                for index, element in enumerate(records):
                    if index % 2 == 0:
                        records_dict[element] = records[index + 1]
                        record_values.append(element)
                # locale.setlocale(locale.LC_ALL, "de_DE.UTF-8")
                record_values = sorted(record_values, key=locale.strxfrm)
                for v in record_values:
                    result_values.append(v)
                    result_values.append(records_dict[v])
                results.facets['facet_fields'][key] = result_values
        return results
