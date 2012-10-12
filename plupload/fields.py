# -*- coding: utf-8 -*-
from django import forms
from django.db.models.fields import Field

from .widgets import PluploadWidget

class PluploadFormField(forms.CharField):
    widget = PluploadWidget

    def __init__(self, *args, **kwargs):
        self.directory = kwargs.pop('directory', None)
        super(PluploadFormField, self).__init__(*args, **kwargs)
