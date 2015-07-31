# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WatchList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='WatchListItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('desired_price', models.FloatField(default=0.0)),
                ('item', models.ForeignKey(related_name='watchlistitems', to='items.Item')),
            ],
        ),
        migrations.AddField(
            model_name='watchlist',
            name='items',
            field=models.ManyToManyField(related_name='watchlists', to='watchlists.WatchListItem'),
        ),
    ]
