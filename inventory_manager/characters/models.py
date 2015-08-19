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
        return super(ActiveOrderManager, self).get_queryset().filter(order_state='active')


class Character(models.Model):

    """
    A model representing a single character
    """
    # Relationships
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

    # Relationships
    character = models.ForeignKey(Character, related_name='assets')
    item = models.ForeignKey(Item, related_name='assets')
    solar_system = models.ForeignKey(SolarSystem, null=True, related_name='assets')
    station = models.ForeignKey(Station, null=True, related_name='assets')

    quantity = models.IntegerField()
    unique_item_id = models.BigIntegerField()
    flag = models.SmallIntegerField()
    packaged = models.BooleanField()

    class Meta:
        ordering = ['item__type_name']

    def __unicode__(self):
        return '{} ({})'.format(self.character.name, self.item.type_name)


class Order(models.Model):

    """
    A model representing a single market order
    """

    # Relationships
    character = models.ForeignKey(Character, related_name='orders')
    item = models.ForeignKey(Item, related_name='orders')
    station = models.ForeignKey(Station, related_name='orders')

    order_id = models.BigIntegerField(unique=True)
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

    def __unicode__(self):
        return 'Character: {}, Item: {}'.format(self.character.name, self.item.type_name)
