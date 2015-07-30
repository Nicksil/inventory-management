from __future__ import absolute_import

import logging

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

logger = logging.getLogger(__name__)


def fetch_assets(api_key, char_id):
    api = evelink.api.API(api_key=api_key)
    char_api = evelink.char.Char(char_id, api)

    return char_api.assets().result


def save_assets(assets, character):
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
                logger.exception(e)


def asset_update(request, pk):
    character = Character.objects.get(pk=pk)
    char_id = character.char_id
    api_key = (character.key_id, character.v_code)

    assets = fetch_assets(api_key, char_id)
    save_assets(assets, character)

    return redirect('characters:asset_list', pk=pk)


def asset_list_view(request, pk):
    character = Character.objects.get(pk=pk)
    assets = character.assets.all()

    return render(
        request,
        'characters/asset_list_view.html',
        {'assets': assets, 'character': character}
    )


def character_delete_view(request, pk):
    Character.objects.get(pk=pk).delete()

    return redirect('characters:list')


def character_detail_view(request, pk):
    character = Character.objects.get(pk=pk)

    return render(
        request,
        'characters/character_detail_view.html',
        {'character': character}
    )


def character_list_view(request):
    user = request.user
    characters = user.characters.all()

    return render(
        request,
        'characters/character_list_view.html',
        {'characters': characters}
    )


def character_add_view(request):
    if request.method == 'POST':
        user = request.user
        key_id = int(request.POST['key_id'])
        v_code = request.POST['v_code']

        characters = fetch_characters((key_id, v_code))
        parsed_characters = parse_characters(characters.result)

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
    api = evelink.api.API(api_key=api_key)
    acct = evelink.account.Account(api=api)
    characters = acct.characters()

    return characters


def parse_characters(characters):
    chars = []
    for c in characters:
        chars.append(
            (characters[c]['id'], characters[c]['name']),
        )

    return chars


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                _login(request, user)
                return redirect('index')
            else:
                # Handle disabled account w/loggin
                pass
        else:
            # Handle invalid login w/logging
            pass

    return render(request, 'characters/login.html')


def logout(request):
    _logout(request)

    return redirect('index')
