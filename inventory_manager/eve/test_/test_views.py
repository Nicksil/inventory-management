# -*- coding: utf-8 -*-
from __future__ import absolute_import
import mock

from django.test import TestCase

from eve.models import Price
from eve.views import fetch_price_data
from eve.views import save_price_data


class TestEveViews(TestCase):

    fixtures = ['eve.json']

    @classmethod
    def setUpTestData(cls):
        cls.price_data = {
            35: {
                'all': {
                    'avg': 8.73,
                    'max': 14.94,
                    'median': 8.0,
                    'min': 5.05,
                    'percentile': 5.05,
                    'stddev': 2.57,
                    'volume': 462874583
                },
                'buy': {
                    'avg': 7.93,
                    'max': 12.01,
                    'median': 7.39,
                    'min': 5.05,
                    'percentile': 11.23,
                    'stddev': 1.77,
                    'volume': 395414000
                },
                'id': 35,
                'sell': {
                    'avg': 13.39,
                    'max': 14.94,
                    'median': 13.99,
                    'min': 9.43,
                    'percentile': 11.41,
                    'stddev': 1.67,
                    'volume': 67460583
                }
            }
        }

    @mock.patch('evelink.thirdparty.eve_central.EVECentral.market_stats')
    def test_fetch_price_data(self, mock_market_stats):
        mock_market_stats.return_value = ('price_data')

        # Check for use w/regions (default region ID 10000048) argument
        fetch_price = fetch_price_data([1, 2, 3])
        self.assertEqual(('price_data', 10000048), fetch_price)

        # Check for use w/system argument
        jita_solar_system_id = 30000142
        fetch_price = fetch_price_data([1, 2, 3], system=jita_solar_system_id)
        self.assertEqual(('price_data', jita_solar_system_id), fetch_price)

    def test_save_price_data_using_region(self):
        # Check that no Price objects are in DB
        prices = Price.objects.all()
        self.assertEqual(0, len(prices))

        # Save new price object to DB
        save_price_data((self.price_data, 10000002))

        # Check that one price record in DB
        prices = Price.objects.all()
        self.assertEqual(1, len(prices))

    def test_save_price_data_using_system(self):
        # Check that no Price objects are in DB
        prices = Price.objects.all()
        self.assertEqual(0, len(prices))

        # Save new price object to DB
        save_price_data((self.price_data, 30000142))

        # Check that one price record in DB
        prices = Price.objects.all()
        self.assertEqual(1, len(prices))
