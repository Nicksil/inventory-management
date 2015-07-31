# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.contrib.auth import authenticate
from django.contrib.auth import login as _login
from django.contrib.auth import logout as _logout
from django.shortcuts import redirect
from django.shortcuts import render
import evelink.api
import evelink.account
import evelink.char

from .models import Asset
from .models import Character
from items.models import Item


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
    assets = char_api.assets().result

    return assets


def prepare_assets(assets, character):
    """
    Prepares dict of assets for saving to Asset model

    :param dict assets: Dictionary of assets
    :param character: Instance of :class:`Character` model
    :return: List of tuples of :class:`Asset` objects
    :rtype: list

    Sample dict format::

       >>> {
               60005485: {
                   'contents': [
                       {
                           'id': <13-digit int>,
                           'item_type_id': <short int>,
                           'location_flag': 4,
                           'location_id': <8-digit int>,
                           'packaged': True,
                           'quantity': 2200
                       }
                   ],
                   'location_id': <8-digit int>
               },
               60012643: {
                   'contents': [
                       {
                           'id': <13-digit int>,
                           'item_type_id': <short int>,
                           'location_flag': 4,
                           'location_id': <8-digit int>,
                           'packaged': False,
                           'quantity': 1,
                           'raw_quantity': -1
                       },
                       {
                           'contents': [
                               {
                                   'id': <13-digit int>,
                                   'item_type_id': <short int>,
                                   'location_flag': 27,
                                   'location_id': <8-digit int>,
                                   'packaged': False,
                                   'quantity': 1,
                                   'raw_quantity': -1
                               }
                           ],
                           'id': <13-digit int>,
                           'item_type_id': <short int>,
                           'location_flag': 4,
                           'location_id': <8-digit int>,
                           'packaged': False,
                           'quantity': 1,
                           'raw_quantity': -1
                       },
                       {
                           'id': <13-digit int>,
                           'item_type_id': <short int>,
                           'location_flag': 4,
                           'location_id': <8-digit int>,
                           'packaged': True,
                           'quantity': 8
                       },
                       {
                           'contents': [
                               {
                                   'id': <13-digit int>,
                                   'item_type_id': <short int>,
                                   'location_flag': 27,
                                   'location_id': <8-digit int>,
                                   'packaged': False,
                                   'quantity': 1,
                                   'raw_quantity': -1
                               }
                           ],
                           'id': <13-digit int>,
                           'item_type_id': <short int>,
                           'location_flag': 4,
                           'location_id': <8-digit int>,
                           'packaged': False,
                           'quantity': 1,
                           'raw_quantity': -1
                       }
                   ],
                   'location_id': <8-digit int>
               }
           }
    """

    asset_list = []
    for a in assets.itervalues():
        for asset in a['contents']:
            _asset = {
                'character': character,
                'item': Item.objects.get(type_id=asset['item_type_id']),
                'unique_item_id': asset['id'],
                'location_id': asset['location_id'],
                'quantity': asset['quantity'],
                'flag': asset['location_flag'],
                'packaged': asset['packaged'],
            }
            asset_list.append(Asset(**_asset))

    return asset_list


def save_assets(assets):
    """
    Saves :class:`Asset` objects in bulk

    :param list assets: List of tuples of Asset objects
    """

    Asset.objects.bulk_create(assets)


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
    characters = acct.characters().result

    return characters


def prepare_characters(user, characters, api_key):
    """
    Prepares dict of characters for saving to Character model

    :param user: Instance of :class:`User` model
    :param dict characters: Dictionary of characters
    :param tuple api_key: Tuple of (key_id, v_code)
    :return: List of tuples of :class:`Character` objects
    :rtype: list
    """

    key_id, v_code = api_key

    character_list = []
    for character in characters.itervalues():
        _character = {
            'user': user,
            'name': character['name'],
            'char_id': character['id'],
            'key_id': key_id,
            'v_code': v_code,
        }
        character_list.append(Character(**_character))

    return character_list


def save_characters(characters):
    """
    Saves :class:`Character` objects in bulk

    :param list characters: List of tuples of Character objects
    """

    Character.objects.bulk_create(characters)


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


def character_delete_view(request, pk):
    """
    Delete a single :class:`Character` object

    :param int pk: Primary key of character
    :return: Redirect to user's list of characters
    """

    Character.objects.get(pk=pk).delete()

    return redirect('characters:list')


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
