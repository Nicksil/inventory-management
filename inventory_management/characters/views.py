# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.contrib.auth import authenticate
from django.contrib.auth import login as _login
from django.contrib.auth import logout as _logout
from django.db import IntegrityError
from django.shortcuts import redirect
from django.shortcuts import render
import evelink.api
import evelink.account
import evelink.char

from .models import Asset
from .models import Character
from items.models import Item


def fetch_assets(api_key, char_id):
    """
    Retrieve character's assets

    :param tuple api_key: Passed in the form of a tuple - (key_id, v_code)
    :param int char_id: Character's ID
    :return: Dictionary of character's assets
    :rtype: dict
    """

    api = evelink.api.API(api_key=api_key)
    char_api = evelink.char.Char(char_id, api)

    return char_api.assets().result


def save_assets(assets, character):
    """
    Save a character's assets using the :class:`Character` model

    :param dict assets: dict of assets as returned by :func:`fetch_assets`
    :param obj character: :class:`Character` object
    :return: None
    :rtype: None
    """

    for loc in assets.itervalues():
        for i in loc['contents']:
            item_type_id = i['item_type_id']
            item = Item.objects.get(type_id=item_type_id)
            unique_item_id = i['id']
            location_id = i['location_id']
            quantity = i['quantity']
            flag = i['location_flag']
            packaged = i['packaged']

            try:
                Asset.objects.create(
                    character=character,
                    item=item,
                    location_id=location_id,
                    unique_item_id=unique_item_id,
                    quantity=quantity,
                    flag=flag,
                    packaged=packaged
                )
            except IntegrityError as e:
                print(e)


def asset_update(request, pk):
    """
    Update a character's assets

    :param int pk: Primary key of character
    :return: Redirect to character's asset list
    """

    character = Character.objects.get(pk=pk)
    char_id = character.char_id
    api_key = (character.key_id, character.v_code)

    assets = fetch_assets(api_key, char_id)
    save_assets(assets, character)

    return redirect('characters:asset_list', pk=pk)


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


def character_delete_view(request, pk):
    """
    Delete a single :class:`Character` object

    :param int pk: Primary key of character
    :return: Redirect to user's list of characters
    """

    Character.objects.get(pk=pk).delete()

    return redirect('characters:list')


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

        characters = fetch_characters((key_id, v_code))
        parsed_characters = parse_characters(characters)

        for p in parsed_characters:
            char_id, name = p
            Character.objects.create(
                user=user,
                name=name,
                char_id=char_id,
                key_id=key_id,
                v_code=v_code,
            )

        return redirect('characters:add')

    return render(request, 'characters/character_add_form.html')


def fetch_characters(api_key):
    """
    Wrapper for API call to EVE's /account/Characters.xml.aspx endpoint,
    returning a list of characters exposed to given API credentials

    :param tuple api_key: A Key ID and Verification Code in the form: (key_id, v_code)
    :return: Dictionary of character data
    :rtype: dict
    """

    api = evelink.api.API(api_key=api_key)
    acct = evelink.account.Account(api=api)
    characters = acct.characters()

    return characters.result


def parse_characters(characters):
    """
    Iterates through dict of characters, creating
    list of tuples of (character ID, character name)

    :param dict characters: Dictionary of characters
    :return: List of tuples in the form: (character ID, character name)
    :rtype: list
    """

    chars = []
    for c in characters:
        chars.append(
            (characters[c]['id'], characters[c]['name']),
        )

    return chars


def login(request):
    """
    A view to display a form for user authentication

    :return: Render function to display view
    """

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                _login(request, user)
                return redirect('index')
            else:
                # Handle disabled account w/logging
                pass
        else:
            # Handle invalid login w/logging
            pass

    return render(request, 'characters/login.html')


def logout(request):
    """
    Destroys a user's session, logging them off

    :return: Redirect to index page
    """

    _logout(request)

    return redirect('index')
