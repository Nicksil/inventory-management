# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging

from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import DeleteView
from django.views.generic import DetailView

from .models import Character
from .models import Order
from .utils import AssetManager
from .utils import CharacterManager
from .utils import OrderManager

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
    char = Character.objects.get(pk=pk)
    char_id = char.char_id
    api_key = char.get_api_key()

    manager = OrderManager(char, char_id, api_key)
    manager.update.delay()

    return redirect('characters:order_list', pk=pk)


def orders_list_view(request, pk):
    character = Character.objects.get(pk=pk)
    orders = character.orders.all().filter(order_state='active') \
        .select_related('station').select_related('item')

    return render(
        request, 'characters/orders_list_view.html',
        {'character': character, 'orders': orders})


def order_qty_threshold_update(request, char_pk, order_pk):
    order = Order.objects.get(pk=order_pk)
    qty_threshold = request.POST['qty_threshold']

    if qty_threshold == '':
        qty_threshold = None

    order.qty_threshold = qty_threshold
    order.save()

    return redirect('characters:order_list', pk=char_pk)
