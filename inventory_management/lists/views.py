from __future__ import absolute_import

from django.shortcuts import redirect
from django.shortcuts import render

from .models import ShoppingList
from characters.models import Character
from items.models import Item


def shoppinglist_detail_view(request, pk):
    shoppinglist = ShoppingList.objects.get(pk=pk)
    return render(
        request,
        'lists/shoppinglist_detail_view.html',
        {'shoppinglist': shoppinglist}
    )


def shoppinglist_item_remove(request, list_pk, item_pk):
    shoppinglist = ShoppingList.objects.get(pk=list_pk)
    item = Item.objects.get(pk=item_pk)
    shoppinglist.items.remove(item)

    return redirect('lists:shoppinglist_update', pk=list_pk)


def shoppinglist_list_view(request):
    shoppinglists = ShoppingList.objects.all()

    return render(
        request,
        'lists/shoppinglist_list_view.html',
        {'shoppinglists': shoppinglists}
    )


def shoppinglist_update_view(request, pk):
    shoppinglist = ShoppingList.objects.get(pk=pk)
    if request.method == 'POST':
        name = request.POST['name']
        items = request.POST['items']

        shoppinglist.name = name
        shoppinglist.save()

        if len(items):
            item_obj = Item.objects.get(type_name=items)
            shoppinglist.items.add(item_obj)

        return redirect('lists:shoppinglist_list')

    return render(
        request,
        'lists/shoppinglist_update_view.html',
        {'shoppinglist': shoppinglist}
    )


def shoppinglist_create_view(request):
    if request.method == 'POST':
        character_obj = Character.objects.get(name=request.POST['character'])
        name = request.POST['name']
        item_obj = Item.objects.get(type_name=request.POST['items'])

        shoppinglist = ShoppingList.objects.create(
            name=name,
            character=character_obj,
        )
        shoppinglist.items.add(item_obj)

        return redirect('lists:shoppinglist_create')

    characters = request.user.characters.all()
    return render(
        request,
        'lists/shoppinglist_create_view.html',
        {'characters': characters}
    )
