# -*- coding: utf-8 -*-
from __future__ import absolute_import

import datetime

from django.test import TestCase

from model_mommy import mommy

from characters.models import Order
from characters.models import strfdelta


class TestCharactersModels(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.order_1 = mommy.make(
            'Order', order_state='active', duration=3, issued=datetime.datetime(2015, 01, 01))
        cls.order_2 = mommy.make(
            'Order', order_state='expired', duration=3, issued=datetime.datetime(2015, 01, 01))
        cls.test_char = mommy.make('Character')

    def test_strfdelta(self):
        utcnow = datetime.datetime(2015, 01, 03)
        tdelta = (self.order_1.issued + datetime.timedelta(days=self.order_1.duration)) - utcnow

        output = strfdelta(tdelta, '{days}d {hours}h {minutes}m {seconds}s')
        self.assertEqual(output, '1d 0h 0m 0s')

    def test_active_order_manager(self):
        all_orders = Order.objects.all()
        self.assertEqual(2, len(all_orders))

        active_orders = Order.active_orders.all()
        self.assertEqual(1, len(active_orders))

    def test_qty_threshold(self):
        order = Order.objects.get(pk=1)

        self.assertFalse(order.met_qty_threshold)

    def test_character_model_get_api_key(self):
        key_id = self.test_char.key_id
        v_code = self.test_char.v_code

        api_key = key_id, v_code
        self.assertEqual(self.test_char.get_api_key(), api_key)

    def test_expires_in(self):
        # Yeah, it's a crappy test...
        return_str = self.order_1.expires_in()
        self.assertIsInstance(return_str, str)
