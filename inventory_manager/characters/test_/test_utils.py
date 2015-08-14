# -*- coding: utf-8 -*-
from __future__ import absolute_import
from collections import namedtuple

import mock
from django.test import TestCase
from evelink import api

from characters.models import Asset as _Asset
from characters.models import Order
from characters.models import Character
from characters.utils import AssetManager
from characters.utils import prepare_orders


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

    def test_prepare_orders_existing_order_object(self):
        # Make sure order currently has 'vol_remaining' attribute at 4000
        existing_order = Order.objects.get(pk=1)
        self.assertEqual(4000, existing_order.vol_remaining)

        updated_order_data = {
            existing_order.order_id: {
                'id': existing_order.order_id,
                'amount_left': 1000,
                'status': existing_order.order_state,
                'price': existing_order.price,
                'timestamp': api.parse_ts("2015-08-07 22:35:00"),
            }
        }

        # Send in an updated version of existing_order
        prepare_orders(updated_order_data, self.character)

        # Make sure order now has 'vol_remaining' attribute at 1000
        existing_order = Order.objects.get(pk=1)
        self.assertEqual(1000, existing_order.vol_remaining)
