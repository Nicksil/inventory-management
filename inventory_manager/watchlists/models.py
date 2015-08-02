# -*- coding: utf-8 -*-
from django.db import models

from eve.models import Item


class WatchListItem(models.Model):

    item = models.ForeignKey(Item, related_name='watchlistitems')
    desired_price = models.FloatField()

    def __unicode__(self):
        return 'Item: {}, Desired Price: {}, Last Sell Price: {}'.format(self.item.type_name, self.desired_price, self.item.prices.last().sell)


class WatchList(models.Model):

    name = models.CharField(max_length=255)
    items = models.ManyToManyField(WatchListItem, related_name='watchlists')

    def __unicode__(self):
        return self.name
