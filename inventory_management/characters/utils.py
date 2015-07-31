# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.db import IntegrityError
import evelink.account
import evelink.api
import evelink.char

from .models import Asset
from .models import Character
from items.models import Item


def fetch_assets(api_key, char_id):
    """
    Retrieve character's assets

    :param tuple api_key: Passed in the form of a tuple - (key_id, v_code)
    :param int char_id: Character's ID
    :return: Dictionary of character's assets
    :rtype: dict
    """

    api = evelink.api.API(api_key=api_key)
    char_api = evelink.char.Char(char_id, api)
    assets = char_api.assets().result

    return assets


def prepare_assets(assets, character):
    """
    Prepares dict of assets for saving to Asset model

    :param dict assets: Dictionary of assets
    :param character: Instance of :class:`Character` model
    :return: List of tuples of :class:`Asset` objects
    :rtype: list

    Sample dict format::

       >>> {
               60005485: {
                   'contents': [
                       {
                           'id': <13-digit int>,
                           'item_type_id': <short int>,
                           'location_flag': 4,
                           'location_id': <8-digit int>,
                           'packaged': True,
                           'quantity': 2200
                       }
                   ],
                   'location_id': <8-digit int>
               },
               60012643: {
                   'contents': [
                       {
                           'id': <13-digit int>,
                           'item_type_id': <short int>,
                           'location_flag': 4,
                           'location_id': <8-digit int>,
                           'packaged': False,
                           'quantity': 1,
                           'raw_quantity': -1
                       },
                       {
                           'contents': [
                               {
                                   'id': <13-digit int>,
                                   'item_type_id': <short int>,
                                   'location_flag': 27,
                                   'location_id': <8-digit int>,
                                   'packaged': False,
                                   'quantity': 1,
                                   'raw_quantity': -1
                               }
                           ],
                           'id': <13-digit int>,
                           'item_type_id': <short int>,
                           'location_flag': 4,
                           'location_id': <8-digit int>,
                           'packaged': False,
                           'quantity': 1,
                           'raw_quantity': -1
                       },
                       {
                           'id': <13-digit int>,
                           'item_type_id': <short int>,
                           'location_flag': 4,
                           'location_id': <8-digit int>,
                           'packaged': True,
                           'quantity': 8
                       },
                       {
                           'contents': [
                               {
                                   'id': <13-digit int>,
                                   'item_type_id': <short int>,
                                   'location_flag': 27,
                                   'location_id': <8-digit int>,
                                   'packaged': False,
                                   'quantity': 1,
                                   'raw_quantity': -1
                               }
                           ],
                           'id': <13-digit int>,
                           'item_type_id': <short int>,
                           'location_flag': 4,
                           'location_id': <8-digit int>,
                           'packaged': False,
                           'quantity': 1,
                           'raw_quantity': -1
                       }
                   ],
                   'location_id': <8-digit int>
               }
           }
    """

    asset_list = []
    for a in assets.itervalues():
        for asset in a['contents']:
            _asset = {
                'character': character,
                'item': Item.objects.get(type_id=asset['item_type_id']),
                'unique_item_id': asset['id'],
                'location_id': asset['location_id'],
                'quantity': asset['quantity'],
                'flag': asset['location_flag'],
                'packaged': asset['packaged'],
            }
            asset_list.append(Asset(**_asset))

    return asset_list


def save_assets(assets):
    """
    Saves :class:`Asset` objects in bulk

    :param list assets: List of tuples of Asset objects
    """

    try:
        Asset.objects.bulk_create(assets)
    except IntegrityError as e:
        print(e)


def fetch_characters(api_key):
    """
    Wrapper for API call to EVE's /account/Characters.xml.aspx endpoint,
    returning a list of characters exposed to given API credentials

    :param tuple api_key: A Key ID and Verification Code in the form: (key_id, v_code)
    :return: Dictionary of character data
    :rtype: dict
    """

    api = evelink.api.API(api_key=api_key)
    acct = evelink.account.Account(api=api)
    characters = acct.characters().result

    return characters


def prepare_characters(user, characters, api_key):
    """
    Prepares dict of characters for saving to Character model

    :param user: Instance of :class:`User` model
    :param dict characters: Dictionary of characters
    :param tuple api_key: Tuple of (key_id, v_code)
    :return: List of tuples of :class:`Character` objects
    :rtype: list
    """

    key_id, v_code = api_key

    character_list = []
    for character in characters.itervalues():
        _character = {
            'user': user,
            'name': character['name'],
            'char_id': character['id'],
            'key_id': key_id,
            'v_code': v_code,
        }
        character_list.append(Character(**_character))

    return character_list


def save_characters(characters):
    """
    Saves :class:`Character` objects in bulk

    :param list characters: List of tuples of Character objects
    """

    try:
        Character.objects.bulk_create(characters)
    except IntegrityError as e:
        print(e)
