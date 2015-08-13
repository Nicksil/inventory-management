# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging

import requests

from .models import Item
from .models import Price
from .models import Station

logger = logging.getLogger(__name__)


def fetch_price_data(type_ids, region_id):
    BASE_MARKET_URL = 'https://public-crest.eveonline.com/market/'
    BASE_TYPE_URL = 'https://public-crest.eveonline.com/types/'

    price_data = []
    for t in type_ids:
        url = '{}{}/orders/sell/'.format(BASE_MARKET_URL, region_id)
        payload = {
            'type': '{}{}/'.format(BASE_TYPE_URL, t),
        }

        resp = requests.get(url, params=payload)
        resp_json = resp.json()

        price_data.append(resp_json)

    return price_data


def save_price_data(price_data):
    for d in price_data:
        for p in d['items']:
            new_price = {}

            type_id = p['type']['id']
            new_price['item'] = Item.objects.get(type_id=type_id)

            try:
                station_id = p['location']['id']
                new_price['station'] = Station.objects.get(station_id=station_id)
            except Station.DoesNotExist as e:
                print(e)
                print('{}: {}'.format(p['location']['name'], p['location']['id']))

            new_price['sell'] = p['price']

            Price.objects.create(**new_price)
