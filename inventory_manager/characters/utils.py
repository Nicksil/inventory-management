# -*- coding: utf-8 -*-
from __future__ import absolute_import

import datetime

from django.db import IntegrityError
import evelink.account
import evelink.api
import evelink.char

from .models import Asset
from .models import Character
from .models import Order
from eve.models import Item
from eve.models import SolarSystem
from eve.models import Station


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
            item = Item.objects.get(type_id=asset['item_type_id'])
            location_id = asset['location_id']

            _asset = {
                'character': character,
                'item': item,
                'unique_item_id': asset['id'],
                'quantity': asset['quantity'],
                'flag': asset['location_flag'],
                'packaged': asset['packaged'],
            }

            try:
                station = Station.objects.get(station_id=location_id)
                _asset.update(station=station)
            except Station.DoesNotExist as e:
                print(e)
                solar_system = SolarSystem.objects.get(solar_system_id=location_id)
                _asset.update(solar_system=solar_system)

            asset_list.append(Asset(**_asset))

            # If sub-contents exist (e.g. items located within a container)
            # Clean this up - it's ewwgly
            if asset.get('contents'):
                for sub_asset in asset['contents']:
                    item = Item.objects.get(type_id=sub_asset['item_type_id'])
                    location_id = sub_asset['location_id']

                    _sub_asset = {
                        'character': character,
                        'item': item,
                        'unique_item_id': sub_asset['id'],
                        'quantity': sub_asset['quantity'],
                        'flag': sub_asset['location_flag'],
                        'packaged': sub_asset['packaged'],
                    }

                    try:
                        station = Station.objects.get(station_id=location_id)
                        _sub_asset.update(station=station)
                    except Station.DoesNotExist as e:
                        print(e)
                        solar_system = SolarSystem.objects.get(solar_system_id=location_id)
                        _sub_asset.update(solar_system=solar_system)

                    asset_list.append(Asset(**_sub_asset))

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


def fetch_orders(api_key, char_id):
    """
    Retrieve character's orders

    :param tuple api_key: Passed in the form of a tuple - (key_id, v_code)
    :param int char_id: Character's ID
    :return: Dictionary of character's orders
    :rtype: dict
    """

    api = evelink.api.API(api_key=api_key)
    char_api = evelink.char.Char(char_id, api)
    orders = char_api.orders().result

    return orders


def prepare_orders(orders, character):
    """
    Finds and updates existing order or prepares
    dict of orders for saving to Order model

    :param dict orders: Dictionary of orders
    :param character: Instance of :class:`Character` model
    :return: List of tuples of :class:`Order` objects
    :rtype: list

    Sample dict format::

       >>> {
               <10-digit int>: {
                   'status': 'expired',
                   'type_id': 24438,
                   'timestamp': <10-digit int>,
                   'price': 708999.99,
                   'account_key': 1000,
                   'escrow': 0.0,
                   'station_id': <8-digit int>,
                   'amount_left': 0,
                   'duration': 0,
                   'id': <10-digit int>,
                   'char_id': <8-digit int>,
                   'range': -1,
                   'amount': 50,
                   'type': 'buy'
               },
               <10-digit int>: {
                   'status': 'active',
                   'type_id': 29668,
                   'timestamp': <10-digit int>,
                   'price': 1000000000.0,
                   'account_key': 1000,
                   'escrow': 0.0,
                   'station_id': <8-digit int>,
                   'amount_left': 1,
                   'duration': 3,
                   'id': <10-digit int>,
                   'char_id': <8-digit int>,
                   'range': 32767,
                   'amount': 1,
                   'type': 'sell'
               },
           }
    """

    order_list = []

    for order in orders.itervalues():
        order_id = order['id']

        try:
            # If order object already exists, grab it, update it, save it
            order_obj = Order.objects.get(order_id=order_id)

            # Update pertinent fields only
            order_obj.vol_remaining = order['amount_left']
            order_obj.order_state = order['status']
            order_obj.price = order['price']
            order_obj.issued = datetime.datetime.utcfromtimestamp(order['timestamp'])

            order_obj.save()
        except Order.DoesNotExist:
            # Order doesn't exist, create new object,
            # adding to list, to be saved in bulk
            item = Item.objects.get(type_id=order['type_id'])
            station = Station.objects.get(station_id=order['station_id'])

            _order = {
                'character': character,
                'item': item,
                'order_id': order_id,
                'station': station,
                'vol_entered': order['amount'],
                'vol_remaining': order['amount_left'],
                'order_state': order['status'],
                'order_type': order['type'],
                'duration': order['duration'],
                'price': order['price'],
                'issued': datetime.datetime.utcfromtimestamp(order['timestamp']),
            }

            order_list.append(Order(**_order))

    return order_list


def save_orders(orders):
    """
    Saves :class:`Order` objects in bulk

    :param list orders: List of tuples of Order objects
    """

    Order.objects.bulk_create(orders)
