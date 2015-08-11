# -*- coding: utf-8 -*-
from __future__ import absolute_import

import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from .models import Asset
from .models import Character
from .models import Order
from .models import strfdelta
from eve.models import Item
from eve.models import Region
from eve.models import Constellation
from eve.models import SolarSystem
from eve.models import Station


class CharactersAppModelsTests(TestCase):

    fixtures = ['characters.json']

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.get(pk=1)
        cls.character = Character.objects.get(pk=1)
        cls.region = Region.objects.get(pk=1)
        cls.constellation = Constellation.objects.get(pk=1)
        cls.solar_system = SolarSystem.objects.get(pk=1)
        cls.station = Station.objects.get(pk=1)
        cls.item = Item.objects.get(pk=1)
        cls.order_active = Order.objects.get(pk=1)
        cls.order_expired = Order.objects.get(pk=2)
        cls.asset_station = Asset.objects.get(pk=1)
        cls.asset_solar_system = Asset.objects.get(pk=2)

    def test_strfdelta_function_returns_correct_string(self):
        issued = datetime.datetime(2015, 7, 10, 17, 53, 48)
        duration = 90
        utc_now = datetime.datetime(2015, 8, 2, 3, 26, 44, 648444)

        tdelta = (issued + datetime.timedelta(days=duration)) - utc_now
        rendered_str = strfdelta(tdelta, '{days}d {hours}h {minutes}m {seconds}s')

        self.assertEqual('67d 14h 27m 3s', rendered_str)

    def test_ActiveOrderManager_model_returns_only_active_orders(self):
        # Test number of all orders first
        all_orders = Order.objects.all()
        self.assertEqual(2, len(all_orders))

        # Test number of active orders only
        active_orders = Order.active_orders.all()
        self.assertEqual(1, len(active_orders))

        # Test the active order is the one we want
        order = active_orders[0]
        self.assertEqual(1234567, order.order_id)

    def test_character_model_method_get_api_key_actually_works(self):
        self.assertTupleEqual(
            (self.character.key_id, self.character.v_code),
            self.character.get_api_key()
        )

    def test_order_model_qty_threshold_check_method(self):
        self.assertFalse(self.order_active.met_qty_threshold)

    def test_order_model_expires_in_method_returns_string(self):
        self.assertIsInstance(self.order_active.expires_in(), str)

    def test_character_model_unicode_method_returns_correct_string(self):
        self.assertEqual(str(self.character), self.character.name)

    def test_asset_model_unicode_method_returns_correct_string(self):
        expected_return_str = '{} ({})'.format(
            self.asset_station.character.name,
            self.asset_station.item.type_name
        )
        self.assertEqual(str(self.asset_station), expected_return_str)

    def test_order_model_unicode_method_returns_correct_string(self):
        expected_return_str = 'Character: {}, Item: {}'.format(
            self.order_active.character.name,
            self.order_active.item.type_name
        )
        self.assertEqual(str(self.order_active), expected_return_str)
