# -*- coding: utf-8 -*-
from __future__ import absolute_import
from collections import namedtuple

from django.test import TestCase

from characters.models import Asset as _Asset
from characters.models import Character
from characters.utils import save_assets


class TestCharactersUtils(TestCase):

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
                            'location_id': 30000142,
                            'packaged': True,
                            'quantity': 2200
                        }
                    ],
                    'location_id': 30000142
                }
            }
        )

    def test_prepare_assets_station_does_not_exist(self):
        char_assets = _Asset.objects.all()

        # Check to make sure only 1 asset record has the solar_system attribute
        self.assertEqual(1, len(char_assets.filter(solar_system__isnull=False)))

        save_assets(self.test_asset.result, self.character)

        # Check if there are now 2 records with a non-null solar_system attribute
        self.assertEqual(2, len(char_assets.filter(solar_system__isnull=False)))
