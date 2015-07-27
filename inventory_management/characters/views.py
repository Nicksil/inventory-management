from django.contrib.auth import authenticate
from django.contrib.auth import login as _login
from django.contrib.auth import logout as _logout
from django.shortcuts import redirect
from django.shortcuts import render


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
