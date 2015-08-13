# -*- coding: utf-8 -*-
from __future__ import absolute_import

import json
import mock

from django.test import TestCase

from eve.models import Item
from eve.models import Price
from eve.models import Region
from eve.test_.data import crest_orders_data
from eve.utils import fetch_price_data
from eve.utils import save_price_data


class TestEveViews(TestCase):

    fixtures = ['eve.json']

    @classmethod
    def setUpTestData(cls):
        cls.item_1 = Item.objects.get(type_name='Sabre')
        cls.item_2 = Item.objects.get(type_name='Svipul')
        cls.type_ids = [cls.item_1.type_id, cls.item_2.type_id]
        cls.region = Region.objects.get(region_name='The Forge')
        cls.region_id = cls.region.region_id

    def test_fetch_price_data(self):
        expected_json_return = json.loads(crest_orders_data)

        with mock.patch('eve.utils.requests') as mock_requests:
            mock_requests.get.return_value = mock_response = mock.Mock()
            mock_response.json.return_value = expected_json_return

            results = fetch_price_data([self.item_1.type_id], 10000002)

        self.assertIsInstance(results, list)

    def test_save_price_data(self):
        self.assertEqual(Price.objects.count(), 0)

        expected_json_return = json.loads(crest_orders_data)

        with mock.patch('eve.utils.requests') as mock_requests:
            mock_requests.get.return_value = mock_response = mock.Mock()
            mock_response.json.return_value = expected_json_return

            results = fetch_price_data([self.item_1.type_id], 10000002)

        save_price_data(results)

        self.assertEqual(Price.objects.count(), 2)

    def test_save_price_data_with_station_exception(self):
        self.assertEqual(Price.objects.count(), 0)

        expected_json_return = json.loads(crest_orders_data)

        # Insert an unrecognized station into last result
        expected_json_return['items'][1]['location']['id'] = 1222234

        with mock.patch('eve.utils.requests') as mock_requests:
            mock_requests.get.return_value = mock_response = mock.Mock()
            mock_response.json.return_value = expected_json_return

            results = fetch_price_data([self.item_1.type_id], 10000002)

        save_price_data(results)

        # Check to see if station attribute is None
        self.assertIsNone(Price.objects.last().station)

        # Check to see if station_name attribute is present
        self.assertIsNotNone(Price.objects.last().station_name)

        self.assertEqual(Price.objects.count(), 2)
