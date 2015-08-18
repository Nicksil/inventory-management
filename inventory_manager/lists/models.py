# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.core.urlresolvers import reverse
from django.db import models

from characters.models import Character
from eve.models import Item


class ShoppingList(models.Model):

    # Relationships
    character = models.ForeignKey(Character, related_name='shoppinglists')
    items = models.ManyToManyField(Item, related_name='shoppinglists')

    name = models.CharField(max_length=255)

    def get_absolute_url(self):
        return reverse('lists:detail', kwargs={'pk': self.pk})

    def __unicode__(self):
        return self.name


class WatchList(models.Model):

    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name
