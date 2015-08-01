# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models

from eve.models import Item


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
    item = models.ForeignKey(Item, related_name='assets')
    unique_item_id = models.BigIntegerField(unique=True)
    location_id = models.IntegerField()
    quantity = models.IntegerField()
    flag = models.SmallIntegerField()
    packaged = models.BooleanField()

    def __unicode__(self):
        return '{} ({})'.format(self.character.name, self.item.type_name)


class Order(models.Model):
    """
    A model representing a single market order
    """

    character = models.ForeignKey(Character, related_name='orders')
    item = models.ForeignKey(Item, related_name='orders')
    order_id = models.BigIntegerField(unique=True)
    station_id = models.IntegerField()
    vol_entered = models.BigIntegerField()
    vol_remaining = models.BigIntegerField()
    order_state = models.CharField(max_length=255)
    order_type = models.CharField(max_length=255)
    duration = models.IntegerField()
    price = models.FloatField()
    issued = models.DateTimeField()

    class Meta:
        ordering = ['-issued']

    def __unicode__(self):
        return 'Character: {}, Item: {}'.format(self.character.name, self.item.type_name)
