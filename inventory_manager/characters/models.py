# -*- coding: utf-8 -*-
import datetime

from django.contrib.auth.models import User
from django.db import models

from eve.models import Item
from eve.models import SolarSystem
from eve.models import Station


# http://stackoverflow.com/a/8907269/1770233
def strfdelta(tdelta, fmt):
    d = {'days': tdelta.days}
    d['hours'], rem = divmod(tdelta.seconds, 3600)
    d['minutes'], d['seconds'] = divmod(rem, 60)

    return fmt.format(**d)


class ActiveOrderManager(models.Manager):

    def get_queryset(self):
        return super(ActiveOrderManager, self).get_queryset().filter(
            order_state='active'
        )


class Character(models.Model):

    """
    A model representing a single character
    """

    user = models.ForeignKey(User, related_name='characters')
    name = models.CharField(max_length=255)
    char_id = models.IntegerField(unique=True)
    key_id = models.IntegerField()
    v_code = models.CharField(max_length=255)

    def get_api_key(self):
        return (self.key_id, self.v_code)

    def __unicode__(self):
        return self.name


class Asset(models.Model):

    """
    A model representing a single character
    """

    character = models.ForeignKey(Character, related_name='assets')
    type_id = models.IntegerField()
    type_name = models.CharField(max_length=255)
    unique_item_id = models.BigIntegerField(unique=True)
    location_id = models.IntegerField()
    location_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    flag = models.SmallIntegerField()
    packaged = models.BooleanField()

    class Meta:
        ordering = ['type_name']

    def save(self, *args, **kwargs):
        if not self.type_name:
            item = Item.objects.get(type_id=self.type_id)
            self.type_name = item.type_name

        # Location may be a station or a solar system. Most assets are located
        # in a station, so try looking that up first. If that fails, the location
        # ID must be that of a solar system.
        if not self.location_name:
            try:
                station = Station.objects.get(station_id=self.location_id)
                self.location_name = station.station_name
            except Station.DoesNotExist:
                solar_system = SolarSystem.objects.get(solar_system_id=self.location_id)
                self.location_name = solar_system.solar_system_name

        super(Asset, self).save(*args, **kwargs)

    def __unicode__(self):
        return '{} ({})'.format(self.character.name, self.type_name)


class Order(models.Model):
    """
    A model representing a single market order
    """

    character = models.ForeignKey(Character, related_name='orders')
    type_id = models.IntegerField()
    type_name = models.CharField(max_length=255)
    order_id = models.BigIntegerField(unique=True, db_index=True)
    station_id = models.IntegerField()
    station_name = models.CharField(max_length=255)
    vol_entered = models.BigIntegerField()
    vol_remaining = models.BigIntegerField()
    order_state = models.CharField(max_length=255)
    order_type = models.CharField(max_length=255)
    duration = models.IntegerField()
    price = models.FloatField()
    issued = models.DateTimeField()
    qty_threshold = models.IntegerField(null=True, blank=True)

    objects = models.Manager()
    active_orders = ActiveOrderManager()

    class Meta:
        ordering = ['-issued']

    @property
    def met_qty_threshold(self):

        return self.vol_remaining <= self.qty_threshold

    def expires_in(self):
        tdelta = (self.issued + datetime.timedelta(days=self.duration)) - datetime.datetime.utcnow()

        return strfdelta(tdelta, '{days}d {hours}h {minutes}m {seconds}s')

    def save(self, *args, **kwargs):
        if not self.type_name:
            item = Item.objects.get(type_id=self.type_id)
            self.type_name = item.type_name
        if not self.station_name:
            station = Station.objects.get(station_id=self.station_id)
            self.station_name = station.station_name

        super(Order, self).save(*args, **kwargs)

    def __unicode__(self):

        return 'Character: {}, Item: {}'.format(self.character.name, self.type_name)
