# -*- coding: utf-8 -*-
from __future__ import absolute_import

import datetime
import logging

from django.db import IntegrityError
import evelink.account
import evelink.api
import evelink.char

from .models import Asset
from .models import Character
from .models import Order
from eve.models import Item
from eve.models import Station
from eve.utils import get_station_or_system

logger = logging.getLogger(__name__)


class AssetManager(object):

    def __init__(self, char, char_id, api_key):
        self.char = char
        self.char_id = char_id
        self.api_key = api_key

    def update(self):
        data = self.fetch()
        parsed = self.parse(data)
        self.save(parsed)

    def fetch(self):
        api = evelink.api.API(api_key=self.api_key)
        char_api = evelink.char.Char(self.char_id, api)
        result = char_api.assets().result
        return result

    def parse(self, assets):
        parsed = []
        for a in assets.itervalues():
            for asset in a['contents']:
                prepped = self.prepare(asset)
                parsed.append(prepped)

                # 'Sub-assets' may exist within an asset
                if asset.get('contents'):
                    for sub_asset in asset['contents']:
                        prepped = self.prepare(sub_asset)
                        parsed.append(prepped)
        return parsed

    def prepare(self, asset):
        type_id = asset['item_type_id']
        location_id = asset['location_id']

        item = Item.objects.get(type_id=type_id)
        location, location_obj = get_station_or_system(location_id)

        prepped = {
            'character': self.char,
            'item': item,
            location: location_obj,
            'unique_item_id': asset['id'],
            'quantity': asset['quantity'],
            'flag': asset['location_flag'],
            'packaged': asset['packaged'],
        }
        return prepped

    def save(self, assets):
        for asset in assets:
            try:
                Asset.objects.create(**asset)
            except IntegrityError as e:
                logger.exception(e)


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

    logger.info(characters)
    return characters


def save_characters(user, characters, api_key):
    """
    Prepares dict of characters for saving to Character model

    :param user: Instance of :class:`User` model
    :param dict characters: Dictionary of characters
    :param tuple api_key: Tuple of (key_id, v_code)
    :return: List of tuples of :class:`Character` objects
    :rtype: list
    """

    key_id, v_code = api_key

    for character in characters.itervalues():
        _character = {
            'user': user,
            'name': character['name'],
            'char_id': character['id'],
            'key_id': key_id,
            'v_code': v_code,
        }

        try:
            Character.objects.create(**_character)
        except IntegrityError:
            pass


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

    logger.info(orders)
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

    # WARNING: INCREDIBLY DUBIOUS HACK AHEAD
    # Set all orders to 'expired' to weed-out
    # order that SHOULD be expired, but aren't
    # showing as such in the API data. Once we
    # figure out WTF is up with the API data,
    # we'll remove this nasty creature and burn it
    Order.objects.all().update(order_state='expired')

    order_list = []
    for order in orders.itervalues():
        order_id = order['id']

        try:
            # If order exists, update
            order_obj = Order.objects.get(order_id=order_id)

            # Update pertinent fields only
            order_obj.vol_remaining = order['amount_left']
            order_obj.order_state = order['status']
            order_obj.price = order['price']
            order_obj.issued = datetime.datetime.utcfromtimestamp(order['timestamp'])

            order_obj.save()
        except Order.DoesNotExist:
            # Order doesn't exist, create new

            type_id = order['type_id']
            item = Item.objects.get(type_id=type_id)

            station_id = order['station_id']
            station = Station.objects.get(station_id=station_id)

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

    for order in orders:
        try:
            order.save()
        except IntegrityError:
            pass
