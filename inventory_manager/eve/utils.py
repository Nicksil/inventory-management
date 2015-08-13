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

        for entry in resp_json['items']:
            price_data.append(entry)

    return price_data


def save_price_data(price_data):
    for price in price_data:
        type_id = price['type']['id']
        item = Item.objects.get(type_id=type_id)
        sell = price['price']

        new_price = {
            'item': item,
            'sell': sell,
        }

        # Not all stations are included within the SDK
        # therefore, a look-up for Station will fail as
        # no object for that station_id exists
        # In this case, we'll instead just use the
        # station name included within the price_data
        try:
            station_id = price['location']['id']
            station = Station.objects.get(station_id=station_id)
            region = station.region
            solar_system = station.solar_system

            new_price['station'] = station
            new_price['region'] = region
            new_price['solar_system'] = solar_system
        except Station.DoesNotExist as e:
            new_price['station_name'] = price['location']['name']

            logger.exception(e)
            logger.info('Station NOT FOUND:{} - {}'.format(
                price['location']['name'],
                price['location']['id']
                )
            )

        Price.objects.create(**new_price)
