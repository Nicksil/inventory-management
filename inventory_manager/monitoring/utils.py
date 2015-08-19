# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.contrib import messages
from django.shortcuts import redirect

from characters.models import Character


# http://stackoverflow.com/a/434328/1770233
# def chunker(seq, size):
#     return (seq[pos:pos + size] for pos in xrange(0, len(seq), size))


# def is_outbid(order):
#     order_price = order.price

    # Try to get last sell price for item,
    # if not price exists for item yet, return
    # None... for now
    # try:
    #     last_item_price = order.item.prices.last().sell
    # except AttributeError:
    #     print('NO SELL PRICE FOUND FOR {}'.format(order.item.type_name))
    #     return

    # return order_price > last_item_price


def qty_threshold_met_alert(char):
    orders = char.orders.all()

    qty_threshold_met = []
    for order in orders:
        if order.met_qty_threshold:
            qty_threshold_met.append(order)

    return qty_threshold_met


def check_qty_threshold(request, pk):
    char = Character.objects.get(pk=pk)
    orders_to_alert = qty_threshold_met_alert(char)

    if orders_to_alert:
        type_names = ', '.join([x.item.type_name for x in orders_to_alert])
        message_text = 'The following items have met their quantity threshold: {}'.format(
            type_names)
        messages.info(request, message_text)

    return redirect('characters:order_list', pk=pk)
