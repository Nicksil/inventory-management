# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging

from django.shortcuts import redirect
from django.shortcuts import render

from .models import Character
from .utils import fetch_assets
from .utils import fetch_characters
from .utils import fetch_orders
from .utils import prepare_assets
from .utils import prepare_characters
from .utils import prepare_orders
from .utils import save_assets
from .utils import save_characters
from .utils import save_orders

logger = logging.getLogger(__name__)


def asset_list_view(request, pk):
    """
    A view providing a list of assets for a given character

    :param int pk: Primary key of character
    :return: Render function for displaying view
    """

    character = Character.objects.get(pk=pk)
    assets = character.assets.all()

    return render(
        request,
        'characters/asset_list_view.html',
        {'assets': assets, 'character': character}
    )


def asset_update(request, pk):
    """
    Update a character's assets

    :param int pk: Primary key of character
    :return: Redirect to character's asset list
    """

    character = Character.objects.get(pk=pk)
    char_id = character.char_id
    api_key = (character.key_id, character.v_code)

    fetched_assets = fetch_assets(api_key, char_id)
    prepared_assets = prepare_assets(fetched_assets, character)
    save_assets(prepared_assets)

    return redirect('characters:asset_list', pk=pk)


def character_add_view(request):
    """
    Create a new :class:`Character` object

    :return: POST requests: Redirect back to this view.
             GET requests: view render function
    """

    if request.method == 'POST':
        user = request.user
        key_id = int(request.POST['key_id'])
        v_code = request.POST['v_code']

        api_key = (key_id, v_code)
        fetched_characters = fetch_characters(api_key)
        prepared_characters = prepare_characters(
            user,
            fetched_characters,
            api_key
        )
        save_characters(prepared_characters)

        return redirect('characters:list')

    return render(request, 'characters/character_add_form.html')


def character_list_view(request):
    """
    A view providing a list of all user's characters

    :return: Render function for displaying view
    """

    user = request.user
    characters = user.characters.all()

    return render(
        request,
        'characters/character_list_view.html',
        {'characters': characters}
    )


def character_detail_view(request, pk):
    """
    A view providing an interface for a single character

    :param int pk: Primary key of character
    :return: Render function for displaying view
    """

    character = Character.objects.get(pk=pk)

    return render(
        request,
        'characters/character_detail_view.html',
        {'character': character}
    )


def character_delete(request, pk):
    """
    Delete a single :class:`Character` object

    :param int pk: Primary key of character
    :return: Redirect to user's list of characters
    """

    Character.objects.get(pk=pk).delete()

    return redirect('characters:list')


def orders_list_view(request, pk):
    """
    Displays list of orders of character given via `pk`

    :param int pk: Primary key of character
    :return: Redirect to character's list of orders
    """

    character = Character.objects.get(pk=pk)
    orders = character.orders.all().filter(order_state='active').select_related('item').select_related('station')

    return render(
        request,
        'characters/orders_list_view.html',
        {'character': character, 'orders': orders}
    )


def orders_update(request, pk):
    character = Character.objects.get(pk=pk)
    char_id = character.char_id
    api_key = character.get_api_key()

    fetched_orders = fetch_orders(api_key, char_id)
    prepared_orders = prepare_orders(fetched_orders, character)
    save_orders(prepared_orders)

    return redirect('characters:order_list', pk=pk)
