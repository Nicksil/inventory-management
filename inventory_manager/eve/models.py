# -*- coding: utf-8 -*-
from django.db import models


class Item(models.Model):
    """
    A model to represent a single Item or "Type"
    """

    type_id = models.IntegerField(unique=True)
    type_name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.type_name


class Region(models.Model):
    """
    A model to represent a single Region
    """

    region_id = models.IntegerField()
    region_name = models.CharField(max_length=255)

    def __unicode__(self):
        return 'Region: {} - {}'.format(
            self.region_name,
            self.region_id
        )


class Constellation(models.Model):
    """
    A model to represent a single Constellation
    """

    constellation_id = models.IntegerField()
    constellation_name = models.CharField(max_length=255)
    region = models.ForeignKey(Region, related_name='constellations')

    def __unicode__(self):
        return 'Constellation: {} - {}'.format(
            self.constellation_name,
            self.constellation_id
        )


class SolarSystem(models.Model):
    """
    A model to represent a single Solar System
    """

    solar_system_id = models.IntegerField()
    solar_system_name = models.CharField(max_length=255)
    region = models.ForeignKey(Region, related_name='solar_systems')
    constellation = models.ForeignKey(Constellation, related_name='solar_systems')
    security = models.FloatField()

    def __unicode__(self):
        return 'Solar System: {} - {}'.format(
            self.solar_system_name,
            self.solar_system_id
        )


class Station(models.Model):
    """
    A model to represent a single Station
    """

    station_id = models.IntegerField()
    station_name = models.CharField(max_length=255)
    region = models.ForeignKey(Region, related_name='stations')
    constellation = models.ForeignKey(Constellation, related_name='stations')
    solar_system = models.ForeignKey(SolarSystem, related_name='stations')

    def __unicode__(self):
        return 'Station: {} - {}'.format(
            self.station_name,
            self.station_id
        )


class Price(models.Model):
    """
    A model to represent a price point on a single Item
    """

    item = models.ForeignKey(Item, related_name='prices')
    buy = models.FloatField(default=0.0)
    sell = models.FloatField(default=0.0)
    added = models.DateTimeField(auto_now_add=True)
    solar_system = models.ForeignKey(SolarSystem, null=True, related_name='prices')
    region = models.ForeignKey(Region, null=True, related_name='prices')

    def __unicode__(self):
        return '({}, {}): ({}, {})'.format(
            self.item.type_name,
            self.item.type_id,
            self.buy, self.sell
        )
