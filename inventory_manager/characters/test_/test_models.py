# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.test import TestCase

from characters.models import Order


class TestCharactersModels(TestCase):

    fixtures = ['characters.json']

    def test_active_order_manager(self):
        all_orders = Order.objects.all()
        self.assertEqual(2, len(all_orders))

        active_orders = Order.active_orders.all()
        self.assertEqual(1, len(active_orders))

    def test_qty_threshold(self):
        order = Order.objects.get(pk=1)

        self.assertFalse(order.met_qty_threshold)
