# -*- coding: utf-8 -*-
from __future__ import absolute_import
from collections import namedtuple

import mock
from django.test import TestCase

from characters.models import Asset as _Asset
from characters.models import Order as _Order
from characters.models import Character
from characters.utils import AssetManager
from characters.utils import OrderManager


class TestCharactersUtils(TestCase):

    fixtures = ['characters.json']

    @classmethod
    def setUpTestData(cls):
        cls.character = Character.objects.get(pk=1)

        Asset = namedtuple('Asset', ['result'])
        cls.test_asset = Asset(
            {
                60005485: {
                    'contents': [
                        {
                            'id': 1234567890123,
                            'item_type_id': 35,
                            'location_flag': 4,
                            'location_id': 30000142,
                            'packaged': True,
                            'quantity': 2200,
                            'contents': [
                                {
                                    'id': 1234567890133,
                                    'item_type_id': 35,
                                    'location_flag': 4,
                                    'location_id': 30000142,
                                    'packaged': True,
                                    'quantity': 2200
                                }
                            ]
                        }
                    ],
                    'location_id': 30000142
                }
            }
        )

        cls.Order = namedtuple('Order', ['result'])
        cls.test_order_existing = cls.Order(
            {
                12345678: {
                    'status': 'active',
                    'type_id': 35,
                    'timestamp': 1350502273,
                    'price': 708999.99,
                    'account_key': 1000,
                    'escrow': 0.0,
                    'station_id': 60003760,
                    'amount_left': 0,
                    'duration': 0,
                    'id': 12345678,
                    'char_id': 12345,
                    'range': -1,
                    'amount': 50,
                    'type': 'sell'
                }
            }
        )

    @mock.patch('evelink.char.Char.assets')
    def test_asset_manager(self, mock_assets):
        mock_assets.return_value = self.test_asset

        char = self.character
        char_id = char.char_id
        api_key = self.character.get_api_key()

        manager = AssetManager(char, char_id, api_key)
        fetch = manager.fetch()
        self.assertIsInstance(fetch, dict)
        self.assertEqual(fetch, self.test_asset.result)

        parse = manager.parse(fetch)
        self.assertIsInstance(parse, list)

        manager.save(parse)
        last_saved_asset = _Asset.objects.last()
        asset_unique_id = last_saved_asset.unique_item_id
        self.assertEqual(asset_unique_id, parse[1]['unique_item_id'])

    @mock.patch('evelink.char.Char.assets')
    def test_asset_manager_update(self, mock_assets):
        mock_assets.return_value = self.test_asset

        prev_num_assets = _Asset.objects.count()

        char = self.character
        char_id = char.char_id
        api_key = self.character.get_api_key()

        manager = AssetManager(char, char_id, api_key)
        manager.update()

        current_num_assets = _Asset.objects.count()
        self.assertEqual(prev_num_assets + 2, current_num_assets)

    @mock.patch('evelink.char.Char.orders')
    def test_order_manager_save_method_handles_existing_object_correctly(self, mock_orders):
        existing_order = _Order.objects.get(pk=1)
        updated_order = self.Order(
            {
                1234567: {
                    'status': 'expired',
                    'type_id': 35,
                    'timestamp': 1350502273,
                    'price': 100.00,
                    'account_key': 1000,
                    'escrow': 0.0,
                    'station_id': 60003760,
                    'amount_left': 0,
                    'duration': 0,
                    'id': 1234567,
                    'char_id': 12345,
                    'range': -1,
                    'amount': 50,
                    'type': 'sell'
                }
            }
        )
        mock_orders.return_value = updated_order

        self.assertEqual(existing_order.order_state, 'active')

        manager = OrderManager(self.character, self.character.char_id, self.character.get_api_key())
        manager.update()

        existing_order = _Order.objects.get(pk=1)

        self.assertEqual(existing_order.order_state, 'expired')
