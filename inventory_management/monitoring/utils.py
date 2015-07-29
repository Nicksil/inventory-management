from __future__ import absolute_import

import logging

from evelink.thirdparty.eve_central import EVECentral

from items.models import Item
from items.models import Price
from watchlists.models import WatchList

logger = logging.getLogger(__name__)


def update_watchlists():
    watchlists = WatchList.objects.all()

    updated_lists = []
    for watchlist in watchlists:
        # Update pricing on each item within watchlist
        update_item_price(watchlist=watchlist)

        for item in watchlist.items.all():
            desired_price = item.desired_price
            last_price = item.item.prices.last().sell

            if last_price <= desired_price:
                updated_lists.append((watchlist, True, item))
            else:
                updated_lists.append((watchlist, False, item))

    return updated_lists


def update_item_price(shoppinglist=None, watchlist=None):
    if shoppinglist:
        items = shoppinglist.items.all()
    elif watchlist:
        items = watchlist.items.all()
        items = [item.item for item in items]
    else:
        logger.error('Must provide shoppinglist or watchlist')
        raise

    eve_central = EVECentral()
    item_ids = [item.type_id for item in items]

    item_prices = eve_central.market_stats(item_ids, hours=5, system=30000142)

    for item in item_prices:
        item_obj = Item.objects.get(type_id=item)
        buy = item_prices[item]['buy']['max']
        sell = item_prices[item]['sell']['min']
        Price.objects.create(
            item=item_obj,
            buy=buy,
            sell=sell
        )
