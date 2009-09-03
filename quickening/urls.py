# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from apps import app_resolver

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('', app_resolver.url_patterns())
