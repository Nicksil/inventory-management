from __future__ import absolute_import

from django.conf.urls import url

from .views import watchlist_create_view
from .views import watchlist_detail_view
from .views import watchlist_list_view

urlpatterns = [
    url(r'^create/$', watchlist_create_view, name='create'),
    url(r'^list/$', watchlist_list_view, name='list'),
    url(r'^(?P<pk>\d+)/detail/$', watchlist_detail_view, name='detail'),
]
