# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging

from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import DeleteView
from django.views.generic import DetailView

from .models import ShoppingList
from characters.models import Character
from eve.models import Item
from eve.models import Price
from eve.models import Region
from eve.utils import PriceFetcher

logger = logging.getLogger(__name__)


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
        name = request.POST.get('name')
        items = request.POST.get('items')

        if name:
            shoppinglist.name = name
            shoppinglist.save()

        if items:
            items = items.split(', ')
            item_list = []
            for item in items:
                item_list.append(Item.objects.get(type_name__iexact=item))
            shoppinglist.items.add(*item_list)

        return redirect('lists:detail', pk=pk)
    return render(request, 'lists/shoppinglist_form.html', {'shoppinglist': shoppinglist})


def shoppinglist_price_update(request, pk):
    shoppinglist = ShoppingList.objects.get(pk=pk)

    region_id = int(request.POST['region'])

    items = shoppinglist.items.all()
    type_ids = [x.type_id for x in items]

    fetcher = PriceFetcher(type_ids, regions=region_id)
    price_data = fetcher.fetch()

    for price in fetcher.prepare_save(price_data):
        Price.objects.create(**price)

    return redirect('lists:detail', pk=pk)


def shoppinglist_create_view(request):
    chars = request.user.characters.all()
    if request.method == 'POST':
        char_name = request.POST['character']
        char = Character.objects.get(name=char_name)
        name = request.POST.get('name')
        item_names = request.POST.get('items').split(', ')

        items = []
        not_found = []
        for item_name in item_names:
            try:
                items.append(Item.objects.get(type_name__iexact=item_name))
            except Item.DoesNotExist as e:
                not_found.append(item_name)
                logger.exception(e)

        shoppinglist = ShoppingList.objects.create(character=char, name=name)
        shoppinglist.items.add(*items)

        if not_found:
            message_text = 'The item(s) listed were not found in the database: {}'.format(
                ', '.join(not_found).rstrip(', '))
            messages.info(request, message_text)

        return redirect('lists:detail', pk=shoppinglist.pk)
    return render(request, 'lists/shoppinglist_create_view.html', {'characters': chars})
