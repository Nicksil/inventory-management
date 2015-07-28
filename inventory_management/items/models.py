from django.db import models


class Item(models.Model):

    type_id = models.IntegerField(unique=True)
    type_name = models.CharField(max_length=256)

    def __unicode__(self):
        return self.type_name


class Price(models.Model):

    item = models.ForeignKey(Item, related_name='prices')
    buy = models.FloatField(default=0.0)
    sell = models.FloatField(default=0.0)
    added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '({}, {}): ({}, {})'.format(
            self.item.type_name,
            self.item.type_id,
            self.buy, self.sell
        )
