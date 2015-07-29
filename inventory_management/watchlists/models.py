from django.db import models

from items.models import Item


class WatchListItem(models.Model):

    item = models.ForeignKey(Item, related_name='watchlistitems')
    desired_price = models.FloatField(default=0.0)

    def __unicode__(self):
        return '{}: {}'.format(self.item.type_name, self.desired_price)


class WatchList(models.Model):

    name = models.CharField(max_length=256)
    items = models.ManyToManyField(WatchListItem, related_name='watchlists')

    def __unicode__(self):
        return self.name
