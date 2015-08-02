# -*- coding: utf-8 -*-
from __future__ import absolute_import

import datetime

from django.test import TestCase

from .models import strfdelta


class CharactersAppModelsTests(TestCase):

    def test_strfdelta_function_returns_correct_string(self):
        issued = datetime.datetime(2015, 7, 10, 17, 53, 48)
        duration = 90
        utc_now = datetime.datetime(2015, 8, 2, 3, 26, 44, 648444)

        tdelta = (issued + datetime.timedelta(days=duration)) - utc_now
        rendered_str = strfdelta(tdelta, '{days}d {hours}h {minutes}m {seconds}s')

        self.assertEqual('67d 14h 27m 3s', rendered_str)
