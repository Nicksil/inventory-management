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
from inventory_manager.tasks import app

logger = logging.getLogger(__name__)


def convert_ts(ts):
    return datetime.datetime.utcfromtimestamp(ts)


class CharacterManager(object):

    def __init__(self, user, key_id, v_code):
        self.user = user
        self.key_id = key_id
        self.v_code = v_code
        self.api_key = (key_id, v_code)

    @app.task
    def update(self):
        data = self.fetch()
        parsed = self.parse(data)
        self.save(parsed)

    def fetch(self):
        api = evelink.api.API(api_key=self.api_key)
        acct = evelink.account.Account(api=api)

        return acct.characters().result

    def parse(self, chars):
        parsed = []
        for char in chars.itervalues():
            prepped = self.prepare(char)
            parsed.append(prepped)

        return parsed

    def prepare(self, char):
        prepped = {
            'user': self.user,
            'name': char['name'],
            'char_id': char['id'],
            'key_id': self.key_id,
            'v_code': self.v_code,
        }

        return prepped

    def save(self, chars):
        for char in chars:
            try:
                Character.objects.create(**char)
            except IntegrityError as e:
                logger.exception(e)


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

        return char_api.assets().result

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
        # Dirty hack to ensure fresh assets
        self.char.assets.all().delete()

        for asset in assets:
            try:
                Asset.objects.create(**asset)
            except IntegrityError as e:
                logger.exception(e)


class OrderManager(object):

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

        return char_api.orders().result

    def parse(self, orders):
        parsed = []
        for order in orders.itervalues():
            type_id = order['type_id']
            station_id = order['station_id']

            item = Item.objects.get(type_id=type_id)
            station = Station.objects.get(station_id=station_id)

            prepped = {
                'character': self.char,
                'item': item,
                'station': station,
                'order_id': order['id'],
                'vol_entered': order['amount'],
                'vol_remaining': order['amount_left'],
                'order_state': order['status'],
                'order_type': order['type'],
                'duration': order['duration'],
                'price': order['price'],
                'issued': convert_ts(order['timestamp']),
            }
            parsed.append(prepped)

        return parsed

    def save(self, orders):
        # Dirty hack for the time-being
        self.char.orders.all().delete()

        for order in orders:
            Order.objects.create(**order)
