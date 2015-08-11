# -*- coding: utf-8 -*-
from __future__ import absolute_import
from collections import namedtuple

from django.test import TestCase
from evelink import api

from characters.models import Asset as _Asset
from characters.models import Order as Order
from characters.models import Character
from characters.utils import prepare_orders
from characters.utils import save_assets


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
                            'quantity': 2200
                        }
                    ],
                    'location_id': 30000142
                }
            }
        )

    def test_prepare_assets_station_does_not_exist(self):
        char_assets = _Asset.objects.all()

        # Check to make sure only 1 asset record has the solar_system attribute
        self.assertEqual(1, len(char_assets.filter(solar_system__isnull=False)))

        save_assets(self.test_asset.result, self.character)

        # Check if there are now 2 records with a non-null solar_system attribute
        self.assertEqual(2, len(char_assets.filter(solar_system__isnull=False)))

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
