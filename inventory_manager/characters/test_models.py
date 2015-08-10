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
from eve.models import SolarSystem
from eve.models import Station


class CharactersAppModelsTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            'test_user',
            'test_user@elohel.biz',
            'mah_test_password'
        )
        cls.character = Character.objects.create(
            user=cls.user,
            name='Test Character 1',
            char_id=12345,
            key_id=98765,
            v_code='heres_a_v_code_123',
        )
        cls.region = Region.objects.create(
            region_id=10000002,
            region_name='The Forge',
        )
        cls.station = Station.objects.create(
            station_id=60003760,
            station_name='Jita IV - Moon 4 - Caldari Navy Assembly Plant',
            region_id=10000002,
            region_name='The Forge',
            constellation_id=20000020,
            constellation_name='Kimotoro',
            solar_system_id=30000142,
            solar_system_name='Jita',
        )
        cls.solar_system = SolarSystem.objects.create(
            solar_system_id=60003760,
            solar_system_name='Jita IV - Moon 4 - Caldari Navy Assembly Plant',
            region_id=10000002,
            region_name='The Forge',
            constellation_id=20000020,
            constellation_name='Kimotoro',
            security=1.0,
        )
        cls.order_active = Order.objects.create(
            character=cls.character,
            type_id=35,
            type_name='Pyerite',
            order_id=1234567,
            station_id=60003760,
            station_name='Jita IV - Moon 4 - Caldari Navy Assembly Plant',
            vol_entered=50000,
            vol_remaining=40000,
            order_state='active',
            order_type='sell',
            duration=90,
            price=5.00,
            issued=datetime.datetime.now(),
        )
        cls.order_expired = Order.objects.create(
            character=cls.character,
            type_id=35,
            type_name='Pyerite',
            order_id=56789,
            station_id=60003760,
            station_name='Jita IV - Moon 4 - Caldari Navy Assembly Plant',
            vol_entered=50000,
            vol_remaining=40000,
            order_state='expired',
            order_type='sell',
            duration=90,
            price=5.00,
            issued=datetime.datetime.now(),
        )
        cls.pyerite = Item.objects.create(
            type_id=35,
            type_name='Pyerite',
        )
        cls.asset_station = Asset.objects.create(
            character=cls.character,
            type_id=35,
            unique_item_id=123,
            location_id=60003760,
            quantity=50000,
            flag=4,
            packaged=False,
        )
        cls.asset_region = Asset.objects.create(
            character=cls.character,
            type_id=35,
            unique_item_id=1234,
            location_id=10000002,
            quantity=50000,
            flag=4,
            packaged=False,
        )

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
            (98765, 'heres_a_v_code_123'),
            self.character.get_api_key()
        )

    def test_asset_model_save_method(self):
        self.assertEqual('Pyerite', self.asset_station.type_name)
        self.assertEqual(
            'Jita IV - Moon 4 - Caldari Navy Assembly Plant',
            self.asset_station.location_name
        )
        self.assertEqual(
            'The Forge',
            self.asset_region.location_name
        )
