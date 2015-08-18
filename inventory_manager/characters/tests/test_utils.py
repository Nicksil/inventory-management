# -*- coding: utf-8 -*-
from __future__ import absolute_import
from collections import namedtuple

from django.test import TestCase

import mock
from model_mommy import mommy

from characters.models import Asset
from characters.models import Order
from characters.utils import AssetManager
from characters.utils import OrderManager


class TestCharactersUtils(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_char = mommy.make('Character')
        cls.test_item = mommy.make('Item')
        cls.test_station = mommy.make('Station')

        cls.APIResult = namedtuple('APIResult', 'result')

        # Setup mocked return from evelink library
        # request to assets endpoint on EVE API
        unique_asset_id_1 = 1234567890123
        unique_asset_id_2 = 1234567890133
        asset_result = {
            cls.test_station.station_id: {
                'location_id': cls.test_station.station_id,
                'contents': [
                    {
                        'location_flag': 4,
                        'packaged': False,
                        'item_type_id': cls.test_item.type_id,
                        'location_id': cls.test_station.station_id,
                        'id': unique_asset_id_1,
                        'quantity': 10,
                        'contents': [
                            {
                                'location_flag': 13,
                                'packaged': False,
                                'item_type_id': cls.test_item.type_id,
                                'location_id': cls.test_station.station_id,
                                'id': unique_asset_id_2,
                                'quantity': 20
                            }
                        ]
                    }
                ]
            }
        }
        cls.test_evelink_assets_response = cls.APIResult(asset_result)

        # Setup mocked return from evelink library
        # request to orders endpoint on EVE API
        cls.order_id = 1234567890
        cls.test_order = mommy.make('Order', order_id=cls.order_id, order_state='active')
        order_result = {
            cls.order_id: {
                'status': cls.test_order.order_state,
                'type_id': cls.test_item.type_id,
                'timestamp': cls.test_order.issued,
                'price': cls.test_order.price,
                'station_id': cls.test_station.station_id,
                'amount_left': cls.test_order.vol_remaining,
                'duration': cls.test_order.duration,
                'id': cls.order_id,
                'char_id': cls.test_char.char_id,
                'amount': cls.test_order.vol_entered,
                'type': cls.test_order.order_type
            }
        }
        cls.test_evelink_orders_response = cls.APIResult(order_result)

    @mock.patch('evelink.char.Char.assets')
    def test_asset_manager(self, mock_assets):
        mock_assets.return_value = self.test_evelink_assets_response

        char = self.test_char
        char_id = char.char_id
        api_key = self.test_char.get_api_key()

        manager = AssetManager(char, char_id, api_key)
        fetch = manager.fetch()
        self.assertEqual(fetch, self.test_evelink_assets_response.result)

        parse = manager.parse(fetch)
        self.assertIsInstance(parse, list)

        manager.save(parse)
        last_saved_asset = Asset.objects.last()
        asset_unique_id = last_saved_asset.unique_item_id
        self.assertEqual(asset_unique_id, parse[0]['unique_item_id'])

    @mock.patch('evelink.char.Char.assets')
    def test_asset_manager_update(self, mock_assets):
        mock_assets.return_value = self.test_evelink_assets_response

        prev_num_assets = Asset.objects.count()

        char = self.test_char
        char_id = char.char_id
        api_key = self.test_char.get_api_key()

        manager = AssetManager(char, char_id, api_key)
        manager.update()

        current_num_assets = Asset.objects.count()
        self.assertEqual(prev_num_assets + 2, current_num_assets)

    @mock.patch('evelink.char.Char.orders')
    def test_order_manager_save_method_handles_existing_object_correctly(self, mock_orders):
        existing_order = Order.objects.last()
        self.assertEqual(existing_order.order_state, 'active')

        updated_order_result = {
            self.order_id: {
                'status': 'expired',
                'type_id': self.test_item.type_id,
                'timestamp': 1439842260,
                'price': 5.00,
                'station_id': self.test_station.station_id,
                'amount_left': 5000,
                'duration': 90,
                'id': self.order_id,
                'char_id': self.test_char.char_id,
                'amount': 9000,
                'type': 'sell'
            }
        }
        updated_order = self.APIResult(updated_order_result)

        mock_orders.return_value = updated_order

        manager = OrderManager(self.test_char, self.test_char.char_id, self.test_char.get_api_key())
        manager.update()

        existing_order = Order.objects.last()
        self.assertEqual(existing_order.order_state, 'expired')
