from __future__ import absolute_import

from django.conf.urls import url

from .views import shoppinglist_create_view
from .views import shoppinglist_detail_view
from .views import shoppinglist_item_remove
from .views import shoppinglist_list_view
from .views import shoppinglist_update_view
from .views import update_item_prices

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
        shoppinglist_detail_view,
        name='detail'
    ),
    url(
        r'^(?P<pk>\d+)/update/$',
        shoppinglist_update_view,
        name='shoppinglist_update'
    ),
    url(
        r'^(?P<pk>\d+)/update-prices/$',
        update_item_prices,
        name='shoppinglist_update_prices'
    ),
    url(
        r'^(?P<list_pk>\d+)/items/(?P<item_pk>\d+)/remove/$',
        shoppinglist_item_remove,
        name='shoppinglist_item_remove'
    ),
]
