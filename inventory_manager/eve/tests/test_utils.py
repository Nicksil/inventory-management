# -*- coding: utf-8 -*-
from __future__ import absolute_import

import mock

from django.test import TestCase

from eve.models import Item
from eve.models import Region
from eve.models import SolarSystem
from eve.models import Station
from eve.utils import PriceFetcher
from eve.utils import get_station_or_system


class TestEveViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.item_1 = Item.objects.get(type_name='Sabre')
        cls.item_2 = Item.objects.get(type_name='Svipul')
        cls.type_ids = [cls.item_1.type_id, cls.item_2.type_id]
        cls.region = Region.objects.get(region_name='The Forge')
        cls.region_id = cls.region.region_id

        cls.test_price_data = {
            'sell': {
                'min': 10.74,
                'max': 17.4,
                'median': 12.23,
                'volume': 6780164119,
                'percentile': 10.88,
                'stddev': 1.67,
                'avg': 13.15
            },
            'all': {
                'min': 1.01,
                'max': 17.4,
                'median': 11.32,
                'volume': 9534000331,
                'percentile': 6.93,
                'stddev': 2.22,
                'avg': 12.19
            },
            'buy': {
                'min': 5.0,
                'max': 10.69,
                'median': 10.55,
                'volume': 2742836212,
                'percentile': 10.68,
                'stddev': 1.31,
                'avg': 9.88
            },
            'id': 35
        }

        cls.market_stats_raw_return_data = {
            35: {
                'sell': {
                    'min': 10.74,
                    'max': 17.4,
                    'median': 12.23,
                    'volume': 6780164119,
                    'percentile': 10.88,
                    'stddev': 1.67,
                    'avg': 13.15
                },
                'all': {
                    'min': 1.01,
                    'max': 17.4,
                    'median': 11.32,
                    'volume': 9534000331,
                    'percentile': 6.93,
                    'stddev': 2.22,
                    'avg': 12.19
                },
                'buy': {
                    'min': 5.0,
                    'max': 10.69,
                    'median': 10.55,
                    'volume': 2742836212,
                    'percentile': 10.68,
                    'stddev': 1.31,
                    'avg': 9.88
                },
                'id': 35
            }
        }

    def test_get_station_or_system(self):
        station_id = Station.objects.get(pk=1).station_id

        location_name, location_obj = get_station_or_system(station_id)
        self.assertEqual(location_name, 'station')

        solar_system_id = SolarSystem.objects.get(pk=1).solar_system_id

        location_name, location_obj = get_station_or_system(solar_system_id)
        self.assertEqual(location_name, 'solar_system')

    @mock.patch('evelink.thirdparty.eve_central.EVECentral.market_stats')
    def test_eve_central_manager_returns_price_data_dict_using_system(self, mock_market_stats):
        mock_market_stats.return_value = self.market_stats_raw_return_data

        type_ids = [35]
        system = 30000142

        manager = PriceFetcher(type_ids, system=system)
        price_data = manager.fetch().next()

        self.assertEqual(price_data, self.test_price_data)

    @mock.patch('evelink.thirdparty.eve_central.EVECentral.market_stats')
    def test_eve_central_manager_returns_price_data_dict_using_hours(self, mock_market_stats):
        mock_market_stats.return_value = self.market_stats_raw_return_data

        type_ids = [35]
        system = 30000142
        hours = 5

        manager = PriceFetcher(type_ids, hours=hours, system=system)
        price_data = manager.fetch().next()

        self.assertEqual(price_data, self.test_price_data)

    @mock.patch('evelink.thirdparty.eve_central.EVECentral.market_stats')
    def test_eve_central_manager_returns_price_data_dict_using_regions(self, mock_market_stats):
        mock_market_stats.return_value = self.market_stats_raw_return_data

        type_ids = [35]
        regions = 10000002

        manager = PriceFetcher(type_ids, regions=regions)
        price_data = manager.fetch().next()

        self.assertEqual(price_data, self.test_price_data)

    def test_eve_central_manager_raises_exception(self):
        type_ids = [35]

        with self.assertRaises(AttributeError):
            PriceFetcher(type_ids)
