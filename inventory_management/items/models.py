from django.db import models


class Item(models.Model):

    type_id = models.IntegerField(unique=True)
    type_name = models.CharField(max_length=256)

    def __unicode__(self):
        return self.type_name
