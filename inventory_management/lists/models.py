from __future__ import absolute_import

from django.db import models

from characters.models import Character
from items.models import Item


class ShoppingList(models.Model):

    name = models.CharField(max_length=256)
    character = models.ForeignKey(Character, related_name='shoppinglists')
    items = models.ManyToManyField(Item, related_name='shoppinglists')

    def __unicode__(self):
        return self.name
