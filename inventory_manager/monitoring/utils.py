# -*- coding: utf-8 -*-
from __future__ import absolute_import


# http://stackoverflow.com/a/434328/1770233
def chunker(seq, size):
    return (seq[pos:pos + size] for pos in xrange(0, len(seq), size))


def is_outbid(order):
    order_price = order.price

    # Try to get last sell price for item,
    # if not price exists for item yet, return
    # None... for now
    try:
        last_item_price = order.item.prices.last().sell
    except AttributeError:
        print('NO SELL PRICE FOUND FOR {}'.format(order.item.type_name))
        return

    return order_price > last_item_price
