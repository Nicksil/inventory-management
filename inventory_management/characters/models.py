from django.contrib.auth.models import User
from django.db import models

from items.models import Item


class Character(models.Model):

    user = models.ForeignKey(User, related_name='characters')
    name = models.CharField(max_length=256)
    char_id = models.IntegerField()
    key_id = models.IntegerField()
    v_code = models.CharField(max_length=256)

    def __unicode__(self):
        return self.name


class Asset(models.Model):

    character = models.ForeignKey(Character, related_name='assets')
    item = models.ForeignKey(Item, related_name='assets')
    unique_item_id = models.BigIntegerField(unique=True)
    location_id = models.IntegerField()
    quantity = models.IntegerField()
    flag = models.SmallIntegerField()
    packaged = models.BooleanField()

    def __unicode__(self):
        return '{} ({})'.format(self.character.name, self.item.type_name)
