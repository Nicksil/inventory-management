from __future__ import absolute_import

from django.conf.urls import url

from .views import character_add_view
from .views import character_list_view

urlpatterns = [
    url(r'^add/$', character_add_view, name='add'),
    url(r'^list/$', character_list_view, name='list'),
]
