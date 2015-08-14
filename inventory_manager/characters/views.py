# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging

from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import DeleteView
from django.views.generic import DetailView

from .models import Character
from .utils import AssetManager
from .utils import CharacterManager
from .utils import fetch_orders
from .utils import prepare_orders
from .utils import save_orders
from eve.utils import fetch_price_data
from eve.utils import save_price_data

logger = logging.getLogger(__name__)


def character_add_view(request):

    if request.method == 'POST':
        user = request.user
        key_id = int(request.POST['key_id'])
        v_code = request.POST['v_code']

        manager = CharacterManager(user, key_id, v_code)
        manager.update()

        return redirect('characters:list')
    return render(request, 'characters/character_add_form.html')


def character_list_view(request):

    user = request.user
    characters = user.characters.all()

    return render(
        request,
        'characters/character_list_view.html', {'characters': characters})


class CharacterDetailView(DetailView):

    model = Character


class CharacterDelete(DeleteView):

    model = Character
    success_url = reverse_lazy('characters:list')


def asset_list_view(request, pk):
    char = Character.objects.get(pk=pk)

    if request.method == 'POST':
        char_id = char.char_id
        api_key = (char.key_id, char.v_code)

        manager = AssetManager(char, char_id, api_key)
        manager.update()

        return redirect('characters:asset_list', pk=pk)

    assets = char.assets.all() \
        .select_related('item').select_related('station')

    return render(
        request, 'characters/asset_list_view.html',
        {'assets': assets, 'char': char})


def orders_update(request, pk):
    character = Character.objects.get(pk=pk)
    char_id = character.char_id
    api_key = character.get_api_key()

    active_orders = character.orders.filter(order_state='active')
    order_data = []

    for order in active_orders:
        type_id = order.item.type_id
        region_id = order.station.region.region_id
        order_data.append((type_id, region_id))

    new_prices = fetch_price_data(order_data)
    save_price_data(new_prices)

    fetched_orders = fetch_orders(api_key, char_id)
    prepared_orders = prepare_orders(fetched_orders, character)
    save_orders(prepared_orders)

    return redirect('characters:order_list', pk=pk)


def orders_list_view(request, pk):

    character = Character.objects.get(pk=pk)
    orders = character.orders.all().filter(order_state='active') \
        .select_related('station').select_related('item')

    return render(
        request, 'characters/orders_list_view.html',
        {'character': character, 'orders': orders})
