from django.contrib.auth.models import User
from django.db import models


class Character(models.Model):

    user = models.ForeignKey(User, related_name='characters')
    name = models.CharField(max_length=256)
    key_id = models.IntegerField()
    v_code = models.CharField(max_length=256)

    def __unicode__(self):
        return self.name
