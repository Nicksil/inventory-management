# -*- coding: utf-8 -*-
from __future__ import absolute_import

import json
import mock

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from characters.models import Character
from eve.models import Item
from lists.test_.data import crest_orders_data
from lists.models import ShoppingList
from lists.models import WatchList


class TestListsViews(TestCase):

    fixtures = ['lists.json']

    @classmethod
    def setUpTestData(cls):
        cls.character = Character.objects.get(pk=1)
        cls.shoppinglist = ShoppingList.objects.get(pk=1)
        cls.watchlist = WatchList.objects.get(pk=1)

        cls.user_password = 'testing_password'
        cls.user = User.objects.create_user(
            username='testing_user',
            password=cls.user_password,
        )

        cls.price_data = {
            35: {
                'all': {
                    'avg': 8.73,
                    'max': 14.94,
                    'median': 8.0,
                    'min': 5.05,
                    'percentile': 5.05,
                    'stddev': 2.57,
                    'volume': 462874583
                },
                'buy': {
                    'avg': 7.93,
                    'max': 12.01,
                    'median': 7.39,
                    'min': 5.05,
                    'percentile': 11.23,
                    'stddev': 1.77,
                    'volume': 395414000
                },
                'id': 35,
                'sell': {
                    'avg': 13.39,
                    'max': 14.94,
                    'median': 13.99,
                    'min': 9.43,
                    'percentile': 11.41,
                    'stddev': 1.67,
                    'volume': 67460583
                }
            }
        }

    def test_update_item_prices(self):
        shoppinglist_pk = self.shoppinglist.pk
        uri = reverse('lists:update_prices', kwargs={'pk': shoppinglist_pk})

        list_item = self.shoppinglist.items.all()[0]
        list_item_price = list_item.prices.last().sell
        self.assertEqual(list_item_price, 1.00)

        expected_json_return = json.loads(crest_orders_data)

        with mock.patch('eve.utils.requests') as mock_requests:
            mock_requests.get.return_value = mock_response = mock.Mock()
            mock_response.json.return_value = expected_json_return

            response = self.client.get(uri, follow=True)

        list_item = self.shoppinglist.items.all()[0]
        list_item_price = list_item.prices.last().sell
        self.assertEqual(list_item_price, 3.00)

        expected_redirect_uri = reverse('lists:detail', kwargs={'pk': shoppinglist_pk})
        self.assertRedirects(response, expected_redirect_uri)

    def test_shoppinglist_delete_view(self):
        self.assertEqual(1, ShoppingList.objects.count())

        uri = reverse('lists:delete', kwargs={'pk': self.shoppinglist.pk})
        response = self.client.post(uri, follow=True)

        self.assertEqual(0, ShoppingList.objects.count())

        expected_redirect_uri = reverse('lists:list')
        self.assertRedirects(response, expected_redirect_uri)

    def test_shoppinglist_item_remove(self):
        # Confirm item is present in list before deletion
        shoppinglist_item_pk = self.shoppinglist.items.last().pk
        self.assertEqual(1, len(self.shoppinglist.items.filter(pk=shoppinglist_item_pk)))

        uri = reverse(
            'lists:item_remove',
            kwargs={
                'list_pk': self.shoppinglist.pk,
                'item_pk': shoppinglist_item_pk,
            }
        )
        response = self.client.get(uri, follow=True)

        # Confirm item no longer in list
        self.assertEqual(0, len(self.shoppinglist.items.filter(pk=shoppinglist_item_pk)))

        expected_redirect_uri = reverse('lists:update', kwargs={'pk': self.shoppinglist.pk})
        self.assertRedirects(response, expected_redirect_uri)

    def test_shoppinglist_update_view(self):
        # Confirm shoppinglist has correct name to begin test
        start_list_name = self.shoppinglist.name
        self.assertEqual(start_list_name, self.shoppinglist.name)

        uri = reverse('lists:update', kwargs={'pk': self.shoppinglist.pk})
        new_list_name = 'New List Name'

        payload = {
            'name': new_list_name,
            'items': '',
        }

        response = self.client.post(uri, data=payload, follow=True)

        # Query shoppinglist again and check name
        shoppinglist = ShoppingList.objects.get(pk=1)
        self.assertEqual(new_list_name, shoppinglist.name)

        expected_redirect_uri = reverse('lists:detail', kwargs={'pk': self.shoppinglist.pk})
        self.assertRedirects(response, expected_redirect_uri)

    def test_shoppinglist_update_view_adding_item(self):
        # Confirm shoppinglist has correct name and number of items to begin test
        start_list_name = self.shoppinglist.name
        start_num_items = self.shoppinglist.items.count()
        self.assertEqual(start_list_name, self.shoppinglist.name)
        self.assertEqual(1, start_num_items)

        uri = reverse('lists:update', kwargs={'pk': self.shoppinglist.pk})
        new_list_name = 'New List Name'
        new_item = Item.objects.get(pk=2).type_name

        payload = {
            'name': new_list_name,
            'items': new_item,
        }

        response = self.client.post(uri, data=payload, follow=True)

        # Query shoppinglist again and check name, number of item objects
        shoppinglist = ShoppingList.objects.get(pk=1)
        self.assertEqual(new_list_name, shoppinglist.name)
        self.assertEqual(2, shoppinglist.items.count())

        expected_redirect_uri = reverse('lists:detail', kwargs={'pk': self.shoppinglist.pk})
        self.assertRedirects(response, expected_redirect_uri)

    def test_shoppinglist_create_view_get(self):
        self.client.login(username=self.user.username, password=self.user_password)

        uri = reverse('lists:create')
        response = self.client.get(uri)

        self.assertTemplateUsed(response, 'lists/shoppinglist_create_view.html')

    def test_shoppinglist_create_view_post(self):
        self.client.login(username=self.user.username, password=self.user_password)

        # Confirm ShoppingList model has just 1 object associated
        self.assertEqual(1, ShoppingList.objects.count())

        items = Item.objects.all()
        item_names = ', '.join([x.type_name for x in items])
        payload = {
            'character': self.character,
            'name': 'New ShoppingList',
            'items': item_names,
        }

        uri = reverse('lists:create')
        response = self.client.post(uri, data=payload, follow=True)

        # Confirm 2 objects now associated with ShoppingList model
        self.assertEqual(2, ShoppingList.objects.count())

        # Should redirect to new ShoppingList object's detail page
        expected_redirect_uri = reverse('lists:detail', kwargs={'pk': 2})
        self.assertRedirects(response, expected_redirect_uri)

    def test_watchlist_delete(self):
        # Confirm 1 watchlist object
        self.assertEqual(1, WatchList.objects.count())

        uri = reverse('lists:watchlist_delete', kwargs={'pk': self.watchlist.pk})
        response = self.client.get(uri, follow=True)

        # Confirm no watchlists
        self.assertEqual(0, WatchList.objects.count())

        expected_redirect_uri = reverse('lists:list')
        self.assertRedirects(response, expected_redirect_uri)

    def test_watchlist_detail_view(self):
        uri = reverse('lists:watchlist_detail', kwargs={'pk': self.watchlist.pk})
        response = self.client.get(uri)

        self.assertTemplateUsed(response, 'lists/watchlist_detail_view.html')

    def test_watchlist_list_view(self):
        uri = reverse('lists:watchlist_list')
        response = self.client.get(uri)

        self.assertTemplateUsed(response, 'lists/watchlist_list_view.html')
