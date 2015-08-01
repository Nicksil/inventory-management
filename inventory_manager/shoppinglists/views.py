# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.shortcuts import redirect
from django.shortcuts import render

from .models import ShoppingList
from characters.models import Character
from eve.models import Item
from eve.views import fetch_price_data
from eve.views import prepare_price_data
from eve.views import save_prices


def update_item_prices(request, pk):
    """
    Updates item pricing data via the eve-central.com market API

    :param int pk: Primary key for :class:`ShoppingList` instance
    :return: Redirect function to given shoppinglist's detail view
    """

    shoppinglist = ShoppingList.objects.get(pk=pk)
    items = shoppinglist.items.all()
    type_ids = [t.type_id for t in items]

    price_data = fetch_price_data(type_ids)
    prepared_data = prepare_price_data(price_data)
    save_prices(prepared_data)

    return redirect('shoppinglists:detail', pk=pk)


def shoppinglist_delete(request, pk):
    ShoppingList.objects.get(pk=pk).delete()

    return redirect('shoppinglists:list')


def shoppinglist_detail_view(request, pk):
    shoppinglist = ShoppingList.objects.get(pk=pk)

    return render(
        request,
        'shoppinglists/shoppinglist_detail_view.html',
        {'shoppinglist': shoppinglist}
    )


def shoppinglist_item_remove(request, list_pk, item_pk):
    shoppinglist = ShoppingList.objects.get(pk=list_pk)
    item = Item.objects.get(pk=item_pk)
    shoppinglist.items.remove(item)

    return redirect('shoppinglists:update', pk=list_pk)


def shoppinglist_list_view(request):
    shoppinglists = ShoppingList.objects.all()

    return render(
        request,
        'shoppinglists/shoppinglist_list_view.html',
        {'shoppinglists': shoppinglists}
    )


def shoppinglist_update_view(request, pk):
    shoppinglist = ShoppingList.objects.get(pk=pk)

    if request.method == 'POST':
        name = request.POST['name']
        items = request.POST['items']

        shoppinglist.name = name
        shoppinglist.save()

        if len(items):
            item_obj = Item.objects.get(type_name=items)
            shoppinglist.items.add(item_obj)

        return redirect('shoppinglists:detail', pk=pk)

    return render(
        request,
        'shoppinglists/shoppinglist_update_view.html',
        {'shoppinglist': shoppinglist}
    )


def shoppinglist_create_view(request):
    if request.method == 'POST':
        character_obj = Character.objects.get(name=request.POST['character'])
        name = request.POST['name']
        item_obj = Item.objects.get(type_name=request.POST['items'])

        shoppinglist = ShoppingList.objects.create(
            name=name,
            character=character_obj,
        )
        shoppinglist.items.add(item_obj)

        return redirect('shoppinglists:detail', pk=shoppinglist.pk)

    characters = request.user.characters.all()
    return render(
        request,
        'shoppinglists/shoppinglist_create_view.html',
        {'characters': characters}
    )
