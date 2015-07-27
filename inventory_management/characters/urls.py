from __future__ import absolute_import

from django.conf.urls import url

from .views import character_add_view
from .views import character_delete_view
from .views import character_detail_view
from .views import character_list_view

urlpatterns = [
    url(r'^add/$', character_add_view, name='add'),
    url(r'^(?P<pk>\d+)/delete/$', character_delete_view, name='delete'),
    url(r'^(?P<pk>\d+)/detail/$', character_detail_view, name='detail'),
    url(r'^list/$', character_list_view, name='list'),
]
