from __future__ import absolute_import

from django.conf.urls import url

from .views import shoppinglist_create_view
from .views import shoppinglist_list_view
from .views import shoppinglist_update_view

urlpatterns = [
    url(r'^create/$', shoppinglist_create_view, name='shoppinglist_create'),
    url(r'^list/$', shoppinglist_list_view, name='shoppinglist_list'),
    url(r'^(?P<pk>\d+)/update/$', shoppinglist_update_view, name='shoppinglist_update'),
]
