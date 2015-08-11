# -*- coding: utf-8 -*-
from __future__ import absolute_import

from collections import namedtuple
import mock

from django.core.urlresolvers import reverse
from django.test import TestCase

from characters.models import Character


class TestCharactersViews(TestCase):

    fixtures = ['characters.json']

    @classmethod
    def setUpTestData(cls):
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
                            'quantity': 2200
                        }
                    ],
                    'location_id': 60003760
                }
            }
        )

    @mock.patch('evelink.char.Char.assets')
    def test_asset_update(self, mock_assets):
        mock_assets.return_value = self.test_asset
        char_pk = self.character.pk

        uri = reverse('characters:asset_update', kwargs={'pk': char_pk})
        response = self.client.get(uri, follow=True)

        expected_redirect_uri = reverse('characters:asset_list', kwargs={'pk': char_pk})
        self.assertRedirects(response, expected_redirect_uri)
