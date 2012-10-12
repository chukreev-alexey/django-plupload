# -*- coding: utf-8 -*-
import os
import copy
import json

from django import forms
from django.forms import widgets
from django.forms.util import flatatt

from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode


class ButtonInput(widgets.Input):
    input_type = 'button'

class PluploadWidget(forms.FileInput):
    default_button_attrs = {'value': u'Загрузить'}
    button_id_prefix = 'plupload_'
    upload_settings = {} # will setup from PluploadInstance class

    def __init__(self, attrs={}):
        super(PluploadWidget, self).__init__(attrs=attrs)
        self.hidden_widget = forms.HiddenInput()
        button_attrs = copy.deepcopy(attrs)
        #if button_attrs.get('value'):
        #    del button_attrs['value']
        self.button_widget = ButtonInput(dict(self.default_button_attrs, **attrs))

    def get_button_id(self, id_):
        return self.button_id_prefix + id_

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        hidden_attrs = {'id': final_attrs['id']}
        button_id = self.get_button_id(final_attrs['id'])
        button_attrs = {'id': button_id}
        upload_settings = None
        if self.upload_settings:
            self.upload_settings.update({
                'browse_button': button_id
            })
            upload_settings = json.dumps(self.upload_settings)
        return render_to_string('plupload/base_plupload_field.html', {
            'hidden_input': self.hidden_widget.render(name, value, attrs=hidden_attrs),
            'button_input': self.button_widget.render('', '', attrs=button_attrs),
            'button_id': button_id,
            'upload_settings': upload_settings,
        })

    def _media(self):
        return forms.Media(js=(
            settings.STATIC_URL + 'plupload/js/plupload.full.js',
            reverse('plupload-init')
        ))
    media = property(_media)


class HrefWidget(widgets.Widget):

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs)
        if final_attrs.get('value'):
            value = force_unicode(final_attrs['value'])
            del final_attrs['value']
        return mark_safe(u'<a href="#" %s>%s</a>' % (flatatt(final_attrs), value))

class PluploadHrefWidget(PluploadWidget):

    def __init__(self, attrs={}):
        super(PluploadHrefWidget, self).__init__(attrs=attrs)
        self.button_widget = HrefWidget(dict(self.default_button_attrs, **attrs))
