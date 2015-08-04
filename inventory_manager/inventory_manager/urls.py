# -*- coding: utf-8 -*-
from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView

from .auth_views import login
from .auth_views import logout

urlpatterns = [
    url(
        r'^login/$',
        login,
        name='login'
    ),
    url(
        r'^logout/$',
        logout,
        name='logout'
    ),
    url(
        r'^characters/',
        include('characters.urls', namespace='characters')
    ),
    url(
        r'^lists/',
        include('lists.urls', namespace='lists')
    ),
    url(
        r'^admin/',
        include(admin.site.urls)
    ),
    url(
        r'^$',
        TemplateView.as_view(template_name='index.html'),
        name='index'
    )
]
