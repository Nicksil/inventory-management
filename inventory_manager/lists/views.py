# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import DeleteView
from django.views.generic import DetailView

from .models import ShoppingList
from .models import WatchList
from characters.models import Character
from eve.models import Item
from eve.models import Region


class ShoppingListDeleteView(DeleteView):

    model = ShoppingList
    success_url = reverse_lazy('lists:list')


class ShoppingListDetailView(DetailView):

    model = ShoppingList

    def get_context_data(self, **kwargs):
        kwargs['regions'] = Region.objects.all()

        return super(ShoppingListDetailView, self).get_context_data(**kwargs)


def shoppinglist_item_remove(request, list_pk, item_pk):
    shoppinglist = ShoppingList.objects.get(pk=list_pk)
    item = Item.objects.get(pk=item_pk)
    shoppinglist.items.remove(item)

    return redirect('lists:update', pk=list_pk)


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

        return redirect('lists:detail', pk=pk)

    return render(
        request,
        'lists/shoppinglist_update_view.html',
        {'shoppinglist': shoppinglist}
    )


def shoppinglist_create_view(request):
    if request.method == 'POST':
        character = Character.objects.get(name=request.POST['character'])

        name = request.POST['name']
        name = name if not name == '' else None

        # Handle if no items were given
        items = request.POST.get('items').split(', ')
        items = [Item.objects.get(type_name__iexact=x) for x in items]

        shoppinglist = ShoppingList(
            name=name,
            character=character,
        )
        shoppinglist.save()
        shoppinglist.items.add(*items)

        return redirect('lists:detail', pk=shoppinglist.pk)

    characters = request.user.characters.all()
    return render(
        request,
        'lists/shoppinglist_create_view.html',
        {'characters': characters}
    )


# def watchlist_update_view(request, pk):
#     pass
    # watchlist = WatchList.objects.get(pk=pk)

    # if request.method == 'POST':
    #     item = request.POST['item']
    #     desired_price = float(request.POST['desired_price'])

    #     item_obj = Item.objects.get(type_name__iexact=item)
    #     watchlist_item = WatchListItem.objects.create(
    #         item=item_obj,
    #         desired_price=desired_price
    #     )
    #     watchlist.items.add(watchlist_item)

    #     return redirect('lists:detail', pk=pk)

    # return render(
    #     request,
    #     'lists/watchlist_update_view.html',
    #     {'watchlist': watchlist}
    # )


def watchlist_delete(request, pk):
    WatchList.objects.get(pk=pk).delete()

    return redirect('lists:list')


def watchlist_detail_view(request, pk):
    watchlist = WatchList.objects.get(pk=pk)

    return render(
        request,
        'lists/watchlist_detail_view.html',
        {'watchlist': watchlist}
    )


def watchlist_list_view(request):
    watchlists = WatchList.objects.all()

    return render(
        request,
        'lists/watchlist_list_view.html',
        {'watchlists': watchlists}
    )


# def watchlist_create_view(request):
#     pass
    # if request.method == 'POST':
    #     name = request.POST['name']
    #     item = request.POST['item']
    #     desired_price = request.POST['desired_price']

    #     item = Item.objects.get(type_name__iexact=item)

    #     watchlist_item = WatchListItem.objects.create(
    #         item=item,
    #         desired_price=desired_price
    #     )
    #     watchlist = WatchList.objects.create(name=name)
    #     watchlist.items.add(watchlist_item)

    #     return redirect('lists:detail', pk=watchlist.pk)

    # return render(request, 'lists/watchlist_create_view.html')
