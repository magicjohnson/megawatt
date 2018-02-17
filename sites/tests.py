from datetime import date

from decimal import Decimal

from django.test import RequestFactory
from django.test import TestCase

from sites.models import Site, SiteDataRecord
from sites.services import SummaryService
from sites.templatetags.tags import active_url


class SummaryServiceTest(TestCase):
    def setUp(self):
        self.maxDiff = None
        site1 = Site.objects.create(name='Demo Site')
        for a, b in [(12, 16), (20, 100), (20, 80)]:
            SiteDataRecord.objects.create(site=site1, value_a=a, value_b=b, date=date(2018, 2, 1))

        site2 = Site.objects.create(name='ABC Site')
        SiteDataRecord.objects.create(site=site2, value_a=5, value_b=15, date=date(2018, 2, 1))

        site3 = Site.objects.create(name='XYZ Site')
        for a, b in [(5, 15), (5, 15)]:
            SiteDataRecord.objects.create(site=site3, value_a=a, value_b=b, date=date(2018, 2, 1))

    def test_get_summary_data__when_called__should_return__aggregated_summary_data_for_all_sites(self):
        data = SummaryService().get_summary_data()
        self.assertEqual(data, [
            {'site_name': 'Demo Site', 'agg_value_a': Decimal('52.00'), 'agg_value_b': Decimal('196.00')},
            {'site_name': 'ABC Site', 'agg_value_a': Decimal('5.00'), 'agg_value_b': Decimal('15.00')},
            {'site_name': 'XYZ Site', 'agg_value_a': Decimal('10.00'), 'agg_value_b': Decimal('30.00')},
        ])

    def test_get_average_data__when_called__should_return__aggregated_average_data_for_all_sites(self):
        data = SummaryService().get_average_data()
        self.assertEqual(list(data), [
            {'site_name': 'Demo Site', 'agg_value_a': Decimal('17.33'), 'agg_value_b': Decimal('65.33')},
            {'site_name': 'ABC Site', 'agg_value_a': Decimal('5.00'), 'agg_value_b': Decimal('15.00')},
            {'site_name': 'XYZ Site', 'agg_value_a': Decimal('5.00'), 'agg_value_b': Decimal('15.00')},
        ])

    def test_get_average_data_orm__when_called__should_return__aggregated_average_data_for_all_sites(self):
        data = SummaryService().get_average_data_orm()
        self.assertEqual(list(data), [
            {'site_name': 'Demo Site', 'agg_value_a': Decimal('17.33'), 'agg_value_b': Decimal('65.33')},
            {'site_name': 'ABC Site', 'agg_value_a': Decimal('5.00'), 'agg_value_b': Decimal('15.00')},
            {'site_name': 'XYZ Site', 'agg_value_a': Decimal('5.00'), 'agg_value_b': Decimal('15.00')},
        ])


class ActiveUrlTest(TestCase):
    def test_active_url__when_any_of_listed_urls_matched__should_return_active(self):
        self.assertEqual(active_url({'request': RequestFactory().get('/summary/')}, 'summary'), 'active')
        self.assertEqual(active_url({'request': RequestFactory().get('/')}, 'index,site-list'), 'active')
        self.assertEqual(active_url({'request': RequestFactory().get('/sites/')}, 'index,site-list'), 'active')

    def test_active_url__when_url_not_matched__should_return_blank_string(self):
        self.assertEqual(active_url({'request': RequestFactory().get('/summary/')}, 'index,site-list'), '')

    def test_active_url__when_url_has_no_reverse_match_and_is_substring_of_path__should_return_active(self):
        self.assertEqual(active_url({'request': RequestFactory().get('/site/1/')}, 'site'), 'active')

    def test_active_url__when_url_has_no_reverse_match_and_is_not_substring_of_path__should_return_blank_string(self):
        self.assertEqual(active_url({'request': RequestFactory().get('/some-path')}, 'site'), '')
