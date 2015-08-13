# -*- coding: utf-8 -*-
from __future__ import absolute_import

from eve.utils import fetch_price_data
from eve.utils import save_price_data


# http://stackoverflow.com/a/434328/1770233
def chunker(seq, size):
    return (seq[pos:pos + size] for pos in xrange(0, len(seq), size))


def check_price(orders):
    order_dict = {}
    for order in orders:
        region_id = order.station.region.region_id
        type_id = order.item.type_id
        try:
            order_dict[region_id].append(type_id)
        except KeyError:
            order_dict[region_id] = [type_id]

    for region_id, type_ids in order_dict.iteritems():
        fetched_data = fetch_price_data(type_ids, region_id)
        save_price_data(fetched_data)

    data = []
    for order in orders:
        order_price = order.price
        last_price = order.item.prices.last().sell

        if order_price > last_price:
            data.append(order.item.type_name)

    return sorted(data)
