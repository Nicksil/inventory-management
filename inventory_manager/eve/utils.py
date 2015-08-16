# -*- coding: utf-8 -*-
from __future__ import absolute_import

from evelink.thirdparty.eve_central import EVECentral

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


class EVECentralManager(object):

    def __init__(self, type_ids, hours=None, regions=None, system=None):
        self.type_ids = type_ids
        self.hours = hours
        self.regions = regions
        self.system = system

        if self.regions is None and self.system is None:
            raise AttributeError('Must include "regions" or "system" argument')

    def update(self):
        price_data = self.fetch()

        return self.parse(price_data)

    def prepare(self):
        payload = {'type_ids': self.type_ids}

        if self.regions:
            payload['regions'] = self.regions
        else:
            payload['system'] = self.system

        if self.hours:
            payload['hours'] = self.hours

        return payload

    def fetch(self):
        """
        Returns an iterator over the values returned by market API call
        """
        eve_central = EVECentral()
        payload = self.prepare()
        price_data = eve_central.market_stats(**payload)

        return price_data

    def parse(self, price_data):
        return price_data.itervalues()
