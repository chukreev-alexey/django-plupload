# -*- coding: utf-8 -*-
from django.conf.urls.defaults import url, patterns
from . import views

urlpatterns = patterns('',
    url(r'^js/init/$', views.init_vars, name="plupload-init"),
)