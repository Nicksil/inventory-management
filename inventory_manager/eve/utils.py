# -*- coding: utf-8 -*-
from __future__ import absolute_import

from evelink.thirdparty.eve_central import EVECentral

from .models import Item
from .models import Region
from .models import SolarSystem
from .models import Station


def get_station_or_system(location_id):
    """
    Given a location ID, determine whether the ID corresponds to
    a station or a solar system.

    Returns tuple of string of location type and its object:
    ('station', station_obj)
    """

    try:
        location_obj = Station.objects.get(station_id=location_id)
        location = 'station'
    except Station.DoesNotExist:
        location_obj = SolarSystem.objects.get(solar_system_id=location_id)
        location = 'solar_system'

    return (location, location_obj)


class PriceFetcher(object):

    def __init__(self, type_ids, hours=None, regions=None, system=None):
        self.type_ids = type_ids
        self.hours = hours
        self.regions = regions
        self.system = system
        self.station = None
        self.payload = None

        if self.regions is None and self.system is None:
            raise AttributeError('Must include "regions" or "system" argument')

    def fetch(self):
        self.payload = self.prepare_payload()

        return self.via_eve_central()

    def prepare_payload(self):
        payload = {'type_ids': self.type_ids}

        if self.regions:
            payload['regions'] = self.regions
        else:
            payload['system'] = self.system

        if self.hours:
            payload['hours'] = self.hours

        return payload

    def via_eve_central(self):
        eve_central = EVECentral()
        price_data = eve_central.market_stats(**self.payload)

        return price_data.itervalues()

    def prepare_save(self, price_data):
        data_list = []
        for price in price_data:
            type_id = price['id']
            item = Item.objects.get(type_id=type_id)

            region_id = self.regions
            region = Region.objects.get(region_id=region_id)

            data_list.append(
                {
                    'item': item,
                    'region': region,
                    'buy': price['buy']['max'],
                    'sell': price['sell']['min']
                }
            )

        return data_list
