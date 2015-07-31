# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('unique_item_id', models.BigIntegerField(unique=True)),
                ('location_id', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('flag', models.SmallIntegerField()),
                ('packaged', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('char_id', models.IntegerField()),
                ('key_id', models.IntegerField()),
                ('v_code', models.CharField(max_length=256)),
                ('user', models.ForeignKey(related_name='characters', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='asset',
            name='character',
            field=models.ForeignKey(related_name='assets', to='characters.Character'),
        ),
        migrations.AddField(
            model_name='asset',
            name='item',
            field=models.ForeignKey(related_name='assets', to='items.Item'),
        ),
    ]
