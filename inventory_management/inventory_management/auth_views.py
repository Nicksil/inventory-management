# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.contrib.auth import authenticate
from django.contrib.auth import login as _login
from django.contrib.auth import logout as _logout
from django.shortcuts import redirect
from django.shortcuts import render


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
