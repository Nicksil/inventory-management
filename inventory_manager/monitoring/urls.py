# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.conf.urls import url

from .utils import check_qty_threshold

urlpatterns = [
    url(
        r'^char/(?P<pk>\d+)/orders/check-qty-threshold/$',
        check_qty_threshold,
        name='check_qty_threshold'),
]
