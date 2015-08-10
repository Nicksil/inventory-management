# -*- coding: utf-8 -*-
from __future__ import absolute_import

import csv
import os

from eve.models import Region
from eve.models import Constellation
from eve.models import SolarSystem
from eve.models import Station
from eve.models import Item

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def populate_items():
    print('Populating items')
    file_loc = os.path.join(BASE_DIR, 'data', 'invTypes.csv')

    with open(file_loc, 'r') as f:
        reader = csv.reader(f)
        for num, row in enumerate(reader):
            type_id, _, type_name, __ = row
            if num:
                Item.objects.create(
                    type_id=type_id,
                    type_name=unicode(type_name).encode('utf-8').strip(),
                )


def populate_regions():
    print('Populating regions')
    file_loc = os.path.join(BASE_DIR, 'data', 'mapRegions.csv')

    with open(file_loc, 'r') as f:
        reader = csv.reader(f)
        for num, row in enumerate(reader):
            if num:
                region_id, region_name = row
                Region.objects.create(
                    region_id=region_id,
                    region_name=region_name,
                )


def populate_constellations():
    print('Populating constellations')
    file_loc = os.path.join(BASE_DIR, 'data', 'mapConstellations.csv')

    with open(file_loc, 'r') as f:
        reader = csv.reader(f)
        for num, row in enumerate(reader):
            if num:
                region_id, const_id, const_name = row
                region = Region.objects.get(region_id=region_id)
                Constellation.objects.create(
                    constellation_id=const_id,
                    constellation_name=const_name,
                    region=region,
                )


def populate_solar_systems():
    print('Populating solar systems')
    file_loc = os.path.join(BASE_DIR, 'data', 'mapSolarSystems.csv')

    with open(file_loc, 'r') as f:
        reader = csv.reader(f)
        for num, row in enumerate(reader):
            if num:
                region_id, const_id, sys_id, sys_name, sec = row
                region = Region.objects.get(region_id=region_id)
                constellation = Constellation.objects.get(constellation_id=const_id)
                SolarSystem.objects.create(
                    solar_system_id=sys_id,
                    solar_system_name=sys_name,
                    region=region,
                    constellation=constellation,
                    security=sec,
                )


def populate_stations():
    print('Populating stations')
    file_loc = os.path.join(BASE_DIR, 'data', 'staStations.csv')

    with open(file_loc, 'r') as f:
        reader = csv.reader(f)
        for num, row in enumerate(reader):
            if num:
                sta_id, sys_id, const_id, region_id, sta_name = row
                region = Region.objects.get(region_id=region_id)
                constellation = Constellation.objects.get(constellation_id=const_id)
                solar_system = SolarSystem.objects.get(solar_system_id=sys_id)
                Station.objects.create(
                    station_id=sta_id,
                    station_name=sta_name,
                    region=region,
                    constellation=constellation,
                    solar_system=solar_system,
                )


def populate_all():
    populate_items()
    populate_regions()
    populate_constellations()
    populate_solar_systems()
    populate_stations()
