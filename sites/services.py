from collections import defaultdict

from decimal import Decimal
from django.db import connection
from django.db.models import Avg

from sites.models import SiteDataRecord, Site


class SummaryService(object):
    def get_summary_data(self):
        """
        Returns aggregated sum values for A and B for all sites and all data records
        Aggregation is made using pure python
        """
        records = SiteDataRecord.objects.all().prefetch_related('site')
        data = defaultdict(dict)
        for record in records:
            name = record.site.name
            data[name]['site_name'] = name
            data[name].setdefault('agg_value_a', 0)
            data[name].setdefault('agg_value_b', 0)
            data[name]['agg_value_a'] += record.value_a
            data[name]['agg_value_b'] += record.value_b

        return list(data.values())

    def get_average_data(self):
        """
        Returns aggregated average values for A and B for all sites and all data records
        Aggregation is made using raw SQL query
        """
        query = '''
                  SELECT
                    s.name,
                    AVG(r.value_a),
                    AVG(r.value_b)
                  FROM sites_site s
                  LEFT JOIN sites_sitedatarecord r ON r.site_id = s.id
                  GROUP BY s.id
                '''

        with connection.cursor() as cursor:
            cursor.execute(query)

            for name, avg_value_a, avg_value_b in cursor.fetchall():
                yield {
                    'site_name': name,
                    'agg_value_a': round(Decimal(avg_value_a), 2),
                    'agg_value_b': round(Decimal(avg_value_b), 2),
                }

    def get_average_data_orm(self):
        """
        Return the same data as get_average_data, but ORM is used
        """
        sites = Site.objects.annotate(
            agg_value_a=Avg('records__value_a'),
            agg_value_b=Avg('records__value_b'),
        )
        for site in sites:
            yield {
                'site_name': site.name,
                'agg_value_a': round(Decimal(site.agg_value_a), 2),
                'agg_value_b': round(Decimal(site.agg_value_b), 2),
            }


