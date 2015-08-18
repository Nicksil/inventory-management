# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.core.urlresolvers import reverse
from django.test import TestCase

from model_mommy import mommy


class TestListsModels(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.shoppinglist = mommy.make('ShoppingList')

    def test_shoppinglist_get_absolute_url(self):
        uri = reverse('lists:detail', kwargs={'pk': self.shoppinglist.pk})
        self.assertEqual(uri, self.shoppinglist.get_absolute_url())
