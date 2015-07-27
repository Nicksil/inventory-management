from __future__ import absolute_import

from django.conf.urls import url

from .views import character_add_view

urlpatterns = [
    url(r'^add/$', character_add_view, name='add'),
]
