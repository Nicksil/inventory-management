# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.conf.urls import url

from .views import asset_list_view
from .views import asset_update
from .views import character_add_view
from .views import character_delete
from .views import character_detail_view
from .views import character_list_view
from .views import orders_list_view
from .views import orders_update
from .views import threshold_update

urlpatterns = [
    url(
        r'^add/$',
        character_add_view,
        name='add'
    ),
    url(
        r'^$',
        character_list_view,
        name='list'
    ),
    url(
        r'^(?P<pk>\d+)/delete/$',
        character_delete,
        name='delete'
    ),
    url(
        r'^(?P<pk>\d+)/detail/$',
        character_detail_view,
        name='detail'
    ),
    url(
        r'^(?P<pk>\d+)/assets/$',
        asset_list_view,
        name='asset_list'
    ),
    url(
        r'^(?P<pk>\d+)/assets/update/$',
        asset_update,
        name='asset_update'
    ),
    url(
        r'^(?P<pk>\d+)/orders/$',
        orders_list_view,
        name='order_list'
    ),
    url(
        r'^(?P<pk>\d+)/orders/update/$',
        orders_update,
        name='orders_update'
    ),
    url(
        r'^(?P<pk>\d+)/orders/update/qty-threshold/$',
        threshold_update,
        name='threshold_update'
    ),
]
