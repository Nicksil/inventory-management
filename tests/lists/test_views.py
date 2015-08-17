# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from inventory_manager.characters.models import Character
from inventory_manager.lists.models import ShoppingList
from inventory_manager.lists.models import WatchList


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

    def test_shoppinglist_create_view_get(self):
        self.client.login(username=self.user.username, password=self.user_password)

        uri = reverse('lists:create')
        response = self.client.get(uri)

        self.assertTemplateUsed(response, 'lists/shoppinglist_create_view.html')

    def test_shoppinglist_update_view_updates_object_name(self):
        self.client.login(username=self.user.username, password=self.user_password)

        start_name = self.shoppinglist.name
        self.assertEqual(start_name, "Test ShoppingList")

        uri = reverse('lists:update', kwargs={'pk': self.shoppinglist.pk})
        payload = {'name': 'Test ShoppingList Updated'}
        response = self.client.post(uri, data=payload)

        final_name = self.shoppinglist.name

        self.assertEqual(final_name, 'Test ShoppingList Updated')

    def test_shoppinglist_update_view_renders_correct_template(self):
        self.client.login(username=self.user.username, password=self.user_password)

        uri = reverse('lists:update', kwargs={'pk': self.shoppinglist.pk})
        response = self.client.get(uri)

        self.assertTemplateUsed(response, 'lists/shoppinglist_form.html')

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
