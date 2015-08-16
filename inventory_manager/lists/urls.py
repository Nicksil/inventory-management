# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.conf.urls import url

from .views import ShoppingListDeleteView
from .views import ShoppingListDetailView
from .views import shoppinglist_create_view
# from .views import shoppinglist_detail_view
from .views import shoppinglist_item_remove
from .views import shoppinglist_list_view
from .views import ShoppingListUpdateView
# from .views import shoppinglist_update_view
# from .views import watchlist_create_view
from .views import watchlist_delete
from .views import watchlist_detail_view
from .views import watchlist_list_view
# from .views import watchlist_update_view

urlpatterns = [
    url(
        r'^create/$',
        shoppinglist_create_view,
        name='create'
    ),
    url(
        r'^list/$',
        shoppinglist_list_view,
        name='list'
    ),
    url(
        r'^(?P<pk>\d+)/detail/$',
        ShoppingListDetailView.as_view(),
        name='detail'
    ),
    url(
        r'^(?P<pk>\d+)/update/$',
        ShoppingListUpdateView.as_view(),
        name='update'
    ),
    url(
        r'^shoppinglist/(?P<pk>\d+)/delete/$',
        ShoppingListDeleteView.as_view(),
        name='delete'
    ),
    # url(
    #     r'^(?P<pk>\d+)/update-prices/$',
    #     update_item_prices,
    #     name='update_prices'
    # ),
    url(
        r'^(?P<list_pk>\d+)/items/(?P<item_pk>\d+)/remove/$',
        shoppinglist_item_remove,
        name='item_remove'
    ),
    # url(r'^create/$', watchlist_create_view, name='create'),
    url(r'^watchlist/list/$', watchlist_list_view, name='watchlist_list'),
    url(r'^watchlist/(?P<pk>\d+)/detail/$', watchlist_detail_view, name='watchlist_detail'),
    url(r'^watchlist/(?P<pk>\d+)/delete/$', watchlist_delete, name='watchlist_delete'),
    # url(r'^(?P<pk>\d+)/update/$', watchlist_update_view, name='update'),
]
