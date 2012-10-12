# -*- coding: utf-8 -*-

from django import forms
from django.core.exceptions import ImproperlyConfigured
from .options import PluploadInstance

class PluploadInstanceRegister(object):
    """ Регистратор plupload виджетов
    """
    def __init__(self):
        self._registry = {}

    def register(self, key, instance_class=None):
        """
        Регистрируем новый PluploadInstance
        """
        if len(key) != 2:
            raise ImproperlyConfigured("First argument must be 2-items tuple.")
        if not issubclass(key[0], forms.BaseForm):
            raise ImproperlyConfigured("First item in tuple must by BaseForm class.")
        if not key[0].base_fields.get(key[1]) or \
           not isinstance(key[0].base_fields[key[1]], forms.Field):
            raise ImproperlyConfigured("Field %s doesn't exists." % key[1])

        string_key = self.get_string_key(key)
        if not instance_class:
            instance_class = PluploadInstance
        self._registry[key] = instance_class(
            field=key[0].base_fields[key[1]], key=string_key)

    def unregister(self, field):
        """
        Удаляем PluploadInstance из регистрации
        """
        if field not in self._registry:
            raise ValueError('The instance %s is not registered' % name)
        del self._registry[field]

    def get_string_key(self, key):
        return '-'.join(key[0].__module__.split('.') + [key[0].__name__.lower(), key[1]])

    def get_urls(self):
        from django.conf.urls import patterns, url, include
        from .urls import urlpatterns as common_urls
        # Добавляем урлы-обработчики для всех зарегистрированных виджетов.
        urlpatterns = common_urls
        for key, instance_class in self._registry.iteritems():
            urlpatterns += instance_class.urls
        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), 'plupload', 'plupload'

plupload_register = PluploadInstanceRegister()
