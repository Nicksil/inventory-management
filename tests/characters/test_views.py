# -*- coding: utf-8 -*-
from __future__ import absolute_import

from collections import namedtuple
import mock

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from inventory_manager.characters.models import Character


class TestCharactersViews(TestCase):

    fixtures = ['characters.json']

    @classmethod
    def setUpTestData(cls):
        cls.user_password = 'test_password'
        cls.user = User.objects.create_user(
            username='test_user',
            password=cls.user_password
        )
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
                            'location_id': 60003760,
                            'packaged': True,
                            'quantity': 2200,
                            'contents': [
                                {
                                    'id': 1234567891123,
                                    'item_type_id': 35,
                                    'location_flag': 4,
                                    'location_id': 60003760,
                                    'packaged': True,
                                    'quantity': 2200,
                                    'raw_quantity': -1
                                }
                            ],
                        }
                    ],
                    'location_id': 60003760
                }
            }
        )

        Char = namedtuple('Char', ['result'])
        cls.test_char = Char(
            {
                123456: {
                    'id': 123456,
                    'name': 'Test Character',
                    'corp': {
                        'id': 67890,
                        'name': 'Test Corp',
                    },
                    'alliance': {
                        'id': 1234567,
                        'name': 'Test Alliance'
                    }
                }
            }
        )

        Order = namedtuple('Order', ['result'])
        cls.test_order = Order(
            {
                1234567890: {
                    'status': 'active',
                    'type_id': 35,
                    'timestamp': 1350502273,
                    'price': 708999.99,
                    'account_key': 1000,
                    'escrow': 0.0,
                    'station_id': 60003760,
                    'amount_left': 0,
                    'duration': 0,
                    'id': 1234567890,
                    'char_id': 12345,
                    'range': -1,
                    'amount': 50,
                    'type': 'sell'
                }
            }
        )

    @mock.patch('evelink.account.Account.characters')
    def test_character_add_view_post_request(self, mock_characters):
        mock_characters.return_value = self.test_char
        self.client.login(username=self.user.username, password=self.user_password)

        uri = reverse('characters:add')
        response = self.client.post(
            uri,
            data={'key_id': 1234567, 'v_code': 'test_v_code_123'},
            follow=True)

        expected_redirect_uri = reverse('characters:list')
        self.assertRedirects(response, expected_redirect_uri)

    def test_character_add_view_get_request(self):
        uri = reverse('characters:add')
        response = self.client.get(uri)

        self.assertTemplateUsed(response, 'characters/character_add_form.html')

    def test_orders_list_view(self):
        uri = reverse(
            'characters:order_list', kwargs={'pk': self.character.pk})
        response = self.client.get(uri)

        self.assertTemplateUsed(response, 'characters/orders_list_view.html')

    @mock.patch('evelink.char.Char.orders')
    def test_orders_update(self, mock_orders):
        mock_orders.return_value = self.test_order

        uri = reverse(
            'characters:orders_update',
            kwargs={'pk': self.character.pk}
        )
        response = self.client.get(uri, follow=True)

        expected_redirect_uri = reverse(
            'characters:order_list',
            kwargs={'pk': self.character.pk}
        )

        self.assertRedirects(response, expected_redirect_uri)

    def test_asset_list_view_get(self):
        uri = reverse('characters:asset_list', kwargs={'pk': self.character.pk})
        response = self.client.get(uri)

        self.assertTemplateUsed(response, 'characters/asset_list_view.html')

    @mock.patch('evelink.char.Char.assets')
    def test_asset_list_view_post(self, mock_assets):
        mock_assets.return_value = self.test_asset

        uri = reverse('characters:asset_list', kwargs={'pk': self.character.pk})
        response = self.client.post(uri, follow=True)

        expected_redirect_uri = reverse(
            'characters:asset_list',
            kwargs={'pk': self.character.pk}
        )

        self.assertRedirects(response, expected_redirect_uri)
