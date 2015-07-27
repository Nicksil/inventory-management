from __future__ import absolute_import

from django.contrib.auth import authenticate
from django.contrib.auth import login as _login
from django.contrib.auth import logout as _logout
from django.shortcuts import redirect
from django.shortcuts import render

from .models import Character


def character_add_view(request):
    if request.method == 'POST':
        user = request.user
        name = request.POST['name']
        key_id = request.POST['key_id']
        v_code = request.POST['v_code']

        Character.objects.create(
            user=user,
            name=name,
            key_id=key_id,
            v_code=v_code,
        )

        return redirect('characters:add')

    return render(request, 'characters/character_add_form.html')


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
