# -*- coding: utf-8 -*-

from django.shortcuts import render

def init_vars(request):
    return render(request, 'plupload/init_vars.js', {}, content_type='text/javascript')