from __future__ import absolute_import

from django.conf.urls import url

from .views import shoppinglist_create_view

urlpatterns = [
    url(r'^create/$', shoppinglist_create_view, name='shoppinglist_create'),
]
