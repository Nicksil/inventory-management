from __future__ import absolute_import

from django.contrib.auth import authenticate
from django.contrib.auth import login as _login
from django.contrib.auth import logout as _logout
from django.shortcuts import redirect
from django.shortcuts import render
import evelink.api
import evelink.account

from .models import Character


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
