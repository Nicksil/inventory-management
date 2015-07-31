# -*- coding: utf-8 -*-
from __future__ import absolute_import


from evelink.thirdparty.eve_central import EVECentral

from .models import Item
from .models import Price


def fetch_price_data(type_ids, hours=24, regions=None, system=30000142):
    """
    Get item prices from evecentral.com

    :param list type_ids: List of item type IDs
    :param int hours: Statistics for market orders with a reported
                      time up to X hours hold; Defaults to 24
    :param int regions: Restrict statistics to a region; Can be
                        specified more than once
    :param int system: Restrict statistics to a system; defaults to Jita
    :return: Dictionary of item price data
    :rtype: dict

    Sample dict format::

       >>> {
               11642: {
                   'all': {
                       'avg': 1242880.04,
                       'max': 1597999.98,
                       'median': 1304939.99,
                       'min': 801024.01,
                       'percentile': 938715.23,
                       'stddev': 139305.88,
                       'volume': 7222
                       },
                   'buy': {
                       'avg': 1120692.62,
                       'max': 1165830.78,
                       'median': 1165827.45,
                       'min': 801024.01,
                       'percentile': 1165830.78,
                       'stddev': 92784.58,
                       'volume': 2279
                   },
                   'id': 11642,
                   'sell': {
                       'avg': 1299215.29,
                       'max': 1597999.98,
                       'median': 1280880.0,
                       'min': 1280878.99,
                       'percentile': 1280879.95,
                       'stddev': 113823.7,
                       'volume': 4943
                   }
               }
           }
    """

    eve_central = EVECentral()

    if regions:
        price_data = eve_central.market_stats(type_ids, hours=hours, regions=regions)
    else:
        price_data = eve_central.market_stats(type_ids, hours=hours, system=system)

    return price_data


def prepare_price_data(price_data):
    """
    Prepares dict of item price data for saving to Price model

    :param dict price_data: Dictionary of pricing data
    :return: List of tuples of :class:`Price` objects
    :rtype: list
    """

    price_list = []
    for price in price_data.itervalues():
        _price = {
            'item': Item.objects.get(type_id=price['id']),
            'buy': price['buy']['max'],
            'sell': price['sell']['min'],
        }
        price_list.append(Price(**_price))

    return price_list


def save_prices(prices):
    """
    Saves price data using :class:`Price` model

    :param list prices: List of tuples of :class:`Price` objects
    """

    Price.objects.bulk_create(prices)
