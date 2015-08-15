# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

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


class PriceManager(object):

    def __init__(self, type_ids, regions, system):
        self.type_ids = type_ids
        self.regions = regions
        self.system = system

    def prepare(self):
        payload = {'type_ids': self.type_ids}

        if self.regions:
            payload['regions'] = self.regions
        elif self.system:
            payload['system'] = self.system
        else:
            raise Exception('Must include "regions" or "system" argument')

        return payload
