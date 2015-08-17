# -*- coding: utf-8 -*-
from __future__ import absolute_import
from collections import namedtuple

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

import mock
from model_mommy import mommy

from characters.models import Character
from characters.models import Order


class TestCharactersViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Can't get a correctly mocked User instance using model_mommy, I
        # believe it has something to do with the `create_user` method and
        # `set_password`. For the time-being, create an un-saved, mocked
        # instance of User and use its attributes to create new User object.
        cls.test_user_attribs = mommy.prepare('User')
        cls.test_user = User.objects.create_user(
            username=cls.test_user_attribs.username,
            password=cls.test_user_attribs.password)

        cls.test_char = mommy.make('Character')
        cls.unsaved_test_char = mommy.prepare('Character')

        cls.test_item = mommy.make('Item')
        cls.test_station = mommy.make('Station')

        # Setup mocked return from evelink library
        # request to characters endpoint on EVE API
        APIResult = namedtuple('APIResult', 'result')
        char_result = {
            cls.unsaved_test_char.char_id: {
                'alliance': {
                    'id': 1234,
                    'name': 'test_alliance'
                },
                'corp': {
                    'id': 1234,
                    'name': 'test_corp'
                },
                'id': cls.unsaved_test_char.char_id,
                'name': 'Test Character'
            }
        }
        cls.test_evelink_characters_response = APIResult(char_result)

        # Setup mocked return from evelink library
        # request to orders endpoint on EVE API
        cls.order_id = 1234567890
        order_result = {
            cls.order_id: {
                'status': 'active',
                'type_id': cls.test_item.type_id,
                'timestamp': 1439842260,
                'price': 5.00,
                'station_id': cls.test_station.station_id,
                'amount_left': 5000,
                'duration': 90,
                'id': cls.order_id,
                'char_id': cls.test_char.char_id,
                'amount': 9000,
                'type': 'sell'
            }
        }
        cls.test_evelink_orders_response = APIResult(order_result)

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
                        'content': [
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
        cls.test_evelink_assets_response = APIResult(asset_result)

    @mock.patch('evelink.account.Account.characters')
    def test_character_add_view_post_request(self, mock_characters):
        mock_characters.return_value = self.test_evelink_characters_response

        self.client.login(
            username=self.test_user.username,
            password=self.test_user_attribs.password)

        key_id = self.unsaved_test_char.key_id
        v_code = self.unsaved_test_char.v_code

        uri = reverse('characters:add')
        response = self.client.post(
            uri,
            data={'key_id': key_id, 'v_code': v_code},
            follow=True)

        last_character = Character.objects.last()
        self.assertEqual(last_character.char_id, self.unsaved_test_char.char_id)

        expected_redirect_uri = reverse('characters:list')
        self.assertRedirects(response, expected_redirect_uri)

    def test_character_add_view_get_request(self):
        uri = reverse('characters:add')
        response = self.client.get(uri)

        self.assertTemplateUsed(response, 'characters/character_add_form.html')

    def test_orders_list_view(self):
        uri = reverse(
            'characters:order_list', kwargs={'pk': self.test_char.pk})
        response = self.client.get(uri)

        self.assertTemplateUsed(response, 'characters/orders_list_view.html')

    @mock.patch('evelink.char.Char.orders')
    def test_orders_update(self, mock_orders):
        mock_orders.return_value = self.test_evelink_orders_response

        uri = reverse(
            'characters:orders_update', kwargs={'pk': self.test_char.pk})
        response = self.client.get(uri, follow=True)

        last_order = Order.objects.last()
        self.assertEqual(last_order.order_id, self.order_id)

        expected_redirect_uri = reverse(
            'characters:order_list', kwargs={'pk': self.test_char.pk})
        self.assertRedirects(response, expected_redirect_uri)

    def test_asset_list_view_get(self):
        uri = reverse('characters:asset_list', kwargs={'pk': self.test_char.pk})
        response = self.client.get(uri)

        self.assertTemplateUsed(response, 'characters/asset_list_view.html')

    @mock.patch('evelink.char.Char.assets')
    def test_asset_list_view_post(self, mock_assets):
        mock_assets.return_value = self.test_evelink_assets_response

        uri = reverse('characters:asset_list', kwargs={'pk': self.test_char.pk})
        response = self.client.post(uri, follow=True)

        expected_redirect_uri = reverse(
            'characters:asset_list',
            kwargs={'pk': self.test_char.pk}
        )

        self.assertRedirects(response, expected_redirect_uri)
