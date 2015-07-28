from django.shortcuts import render


def shoppinglist_create_view(request):
    return render(request, 'lists/shoppinglist_create_view.html')
