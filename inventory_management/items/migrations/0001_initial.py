# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type_id', models.IntegerField(unique=True)),
                ('type_name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('buy', models.FloatField(default=0.0)),
                ('sell', models.FloatField(default=0.0)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('item', models.ForeignKey(related_name='prices', to='items.Item')),
            ],
        ),
    ]
