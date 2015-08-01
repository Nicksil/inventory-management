# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.shortcuts import redirect
from django.shortcuts import render

from .models import WatchList
from .models import WatchListItem
from eve.models import Item


def watchlist_update_view(request, pk):
    watchlist = WatchList.objects.get(pk=pk)

    if request.method == 'POST':
        item = request.POST['item']
        desired_price = float(request.POST['desired_price'])

        item_obj = Item.objects.get(type_name__iexact=item)
        watchlist_item = WatchListItem.objects.create(
            item=item_obj,
            desired_price=desired_price
        )
        watchlist.items.add(watchlist_item)

        return redirect('watchlists:detail', pk=pk)

    return render(
        request,
        'watchlists/watchlist_update_view.html',
        {'watchlist': watchlist}
    )


def watchlist_detail_view(request, pk):
    watchlist = WatchList.objects.get(pk=pk)

    return render(
        request,
        'watchlists/watchlist_detail_view.html',
        {'watchlist': watchlist}
    )


def watchlist_list_view(request):
    watchlists = WatchList.objects.all()

    return render(
        request,
        'watchlists/watchlist_list_view.html',
        {'watchlists': watchlists}
    )


def watchlist_create_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        item = request.POST['item']
        desired_price = request.POST['desired_price']

        item = Item.objects.get(type_name__iexact=item)

        watchlist_item = WatchListItem.objects.create(
            item=item,
            desired_price=desired_price
        )
        watchlist = WatchList.objects.create(name=name)
        watchlist.items.add(watchlist_item)

        return redirect('watchlists:detail', pk=watchlist.pk)

    return render(request, 'watchlists/watchlist_create_view.html')
