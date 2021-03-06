# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.conf.urls import url

from .views import ShoppingListDeleteView
from .views import ShoppingListDetailView
from .views import shoppinglist_create_view
from .views import shoppinglist_item_remove
from .views import shoppinglist_list_view
from .views import shoppinglist_price_update
from .views import shoppinglist_update_view

urlpatterns = [
    url(r'^create/$', shoppinglist_create_view, name='create'),
    url(r'^$', shoppinglist_list_view, name='list'),
    url(r'^(?P<pk>\d+)/detail/$', ShoppingListDetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/update/$', shoppinglist_update_view, name='update'),
    url(r'^(?P<pk>\d+)/delete/$', ShoppingListDeleteView.as_view(), name='delete'),
    url(r'^(?P<pk>\d+)/prices/update/$', shoppinglist_price_update, name='price_update'),
    url(
        r'^(?P<list_pk>\d+)/items/(?P<item_pk>\d+)/remove/$',
        shoppinglist_item_remove,
        name='item_remove'),
]
