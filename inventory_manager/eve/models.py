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
    region_id = models.IntegerField()
    region_name = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if not self.region_name:
            region = Region.objects.get(region_id=self.region_id)
            self.region_name = region.region_name

        super(Constellation, self).save(*args, **kwargs)

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
    region_id = models.IntegerField()
    region_name = models.CharField(max_length=255)
    constellation_id = models.IntegerField()
    constellation_name = models.CharField(max_length=255)
    security = models.FloatField()

    def save(self, *args, **kwargs):
        if not self.constellation_name:
            constellation = Constellation.objects.get(
                constellation_id=self.constellation_id
            )
            self.constellation_name = constellation.constellation_name

            region = Region.objects.get(region_id=self.region_id)
            self.region_name = region.region_name

        super(SolarSystem, self).save(*args, **kwargs)

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
    region_id = models.IntegerField()
    region_name = models.CharField(max_length=255)
    constellation_id = models.IntegerField()
    constellation_name = models.CharField(max_length=255)
    solar_system_id = models.IntegerField()
    solar_system_name = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if not self.solar_system_name:
            solar_system = SolarSystem.objects.get(
                solar_system_id=self.solar_system_id
            )
            self.solar_system_name = solar_system.solar_system_name

            constellation = Constellation.objects.get(
                constellation_id=self.constellation_id
            )
            self.constellation_name = constellation.constellation_name

            region = Region.objects.get(region_id=self.region_id)
            self.region_name = region.region_name

        super(Station, self).save(*args, **kwargs)

    def __unicode__(self):
        return 'Station: {} - {}'.format(
            self.station_name,
            self.station_id
        )


class Price(models.Model):
    """
    A model to represent a price point on a single Item
    """

    _type = models.ForeignKey(Item, related_name='prices')
    type_id = models.IntegerField()
    type_name = models.CharField(max_length=255)
    buy = models.FloatField()
    sell = models.FloatField()
    added = models.DateTimeField(auto_now_add=True)
    location_id = models.IntegerField()
    location_name = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if not self.type_name:
            item = Item.objects.get(type_id=self.type_id)
            self.type_name = item.type_name

        if not self.location_name:
            try:
                solar_system = SolarSystem.objects.get(solar_system_id=self.location_id)
                self.location_name = solar_system.solar_system_name
            except SolarSystem.DoesNotExist:
                region = Region.objects.get(region_id=self.location_id)
                self.location_name = region.region_name

        super(Price, self).save(*args, **kwargs)

    def __unicode__(self):
        return '{}: {}'.format(self.type_name, self.sell)
