# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

import mock
from model_mommy import mommy

from lists.models import ShoppingList


class TestListsViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.char = mommy.make('Character')
        cls.region = mommy.make('Region')
        cls.item_1 = mommy.make('Item')
        cls.item_2 = mommy.make('Item')
        cls.item_3 = mommy.make('Item')
        cls.price_1 = mommy.make('Price', item=cls.item_1)
        cls.shoppinglist = mommy.make('ShoppingList')

        cls.shoppinglist.items.add(cls.item_1)

        # Can't get a correctly mocked User instance using model_mommy, I
        # believe it has something to do with the `create_user` method and
        # `set_password`. For the time-being, create an un-saved, mocked
        # instance of User and use its attributes to create new User object.
        cls.test_user_attribs = mommy.prepare('User')
        cls.test_user = User.objects.create_user(
            username=cls.test_user_attribs.username,
            password=cls.test_user_attribs.password)

        cls.price_data = {
            cls.item_1.type_id: {
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
                    'max': cls.price_1.buy,
                    'median': 7.39,
                    'min': 5.05,
                    'percentile': 11.23,
                    'stddev': 1.77,
                    'volume': 395414000
                },
                'id': cls.item_1.type_id,
                'sell': {
                    'avg': 13.39,
                    'max': 14.94,
                    'median': 13.99,
                    'min': cls.price_1.sell,
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
        self.client.login(
            username=self.test_user.username, password=self.test_user_attribs.password)

        uri = reverse('lists:create')
        response = self.client.get(uri)

        self.assertTemplateUsed(response, 'lists/shoppinglist_create_view.html')

    def test_shoppinglist_create_view_post(self):
        self.client.login(
            username=self.test_user.username, password=self.test_user_attribs.password)

        uri = reverse('lists:create')
        payload = {
            'character': self.char,
            'name': 'New List',
            'items': '{}, {}, {}'.format(
                self.item_1.type_name, self.item_2.type_name, self.item_3.type_name)
        }
        response = self.client.post(uri, data=payload, follow=True)

        last_shoppinglist = ShoppingList.objects.last()
        expected_redirect_uri = reverse('lists:detail', kwargs={'pk': last_shoppinglist.pk})
        self.assertRedirects(response, expected_redirect_uri)

    def test_shoppinglist_update_view_updates_object_name(self):
        self.client.login(
            username=self.test_user.username, password=self.test_user_attribs.password)

        start_name = self.shoppinglist.name
        self.assertEqual(start_name, self.shoppinglist.name)

        uri = reverse('lists:update', kwargs={'pk': self.shoppinglist.pk})
        payload = {'name': 'Test ShoppingList Updated'}
        response = self.client.post(uri, data=payload, follow=True)

        # Query the DB once again for same object in order to show changed name
        final_name = ShoppingList.objects.get(pk=self.shoppinglist.pk).name
        self.assertEqual(final_name, 'Test ShoppingList Updated')

        expected_redirect_uri = reverse('lists:detail', kwargs={'pk': self.shoppinglist.pk})
        self.assertRedirects(response, expected_redirect_uri)

    def test_shoppinglist_update_view_updates_object_items(self):
        self.client.login(
            username=self.test_user.username, password=self.test_user_attribs.password)

        # Confirm 1 item associated with shoppinglist
        self.assertEqual(1, self.shoppinglist.items.count())

        uri = reverse('lists:update', kwargs={'pk': self.shoppinglist.pk})
        item_names = '{}, {}'.format(self.item_2.type_name, self.item_3.type_name)
        payload = {'items': item_names}
        response = self.client.post(uri, data=payload, follow=True)

        # Confirm 3 items associated with shoppinglist
        self.assertEqual(3, self.shoppinglist.items.count())

        expected_redirect_uri = reverse('lists:detail', kwargs={'pk': self.shoppinglist.pk})
        self.assertRedirects(response, expected_redirect_uri)

    def test_shoppinglist_update_view_renders_correct_template(self):
        self.client.login(username=self.test_user.username, password=self.test_user.password)

        uri = reverse('lists:update', kwargs={'pk': self.shoppinglist.pk})
        response = self.client.get(uri)

        self.assertTemplateUsed(response, 'lists/shoppinglist_form.html')

    @mock.patch('eve.utils.PriceFetcher.via_eve_central')
    def test_shoppinglist_price_update(self, mock_fetch):
        mock_fetch.return_value = self.price_data.itervalues()
        self.client.login(username=self.test_user.username, password=self.test_user.password)

        region_id = self.region.region_id

        uri = reverse('lists:price_update', kwargs={'pk': self.shoppinglist.pk})
        response = self.client.post(uri, data={'region': region_id}, follow=True)

        expected_redirect_uri = reverse('lists:detail', kwargs={'pk': self.shoppinglist.pk})
        self.assertRedirects(response, expected_redirect_uri)
