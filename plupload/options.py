# -*- coding: utf-8 -*-
import os
import json

from django.core.urlresolvers import reverse
from django.http import HttpResponse

from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST

from . import settings

class PluploadFileNotValid(Exception):
    "Uploaded file is not valid."
    pass

class PluploadInstance(object):
    """
    Описывает поведение конкретного plupload виджета
    """

    default_settings = {
        "runtimes": 'html5,flash,silverlight,html4',
        "max_file_size": '20mb',
        "multi_selection": False,
        "chunk_size": '1mb',
        "flash_swf_url":  settings.STATIC_URL + 'plupload/js/plupload.flash.swf',
        "silverlight_xap_url": settings.STATIC_URL + 'plupload/js/plupload.silverlight.xap',
        "filters": [
            {"title": u"Image files", "extensions": "jpg,jpeg,gif,png"}
        ],
        "headers": {
            'X-Requested-With'  : 'XMLHttpRequest',
            'X-CSRFToken'       : '',
            'X-PluploadKey'     : ''
        }
    }
    upload_settings = {}

    def __init__(self, field, key):
        self.field = field
        self.key = key
        self.upload_settings['url'] = '/plupload/'+self.key+'/upload/'
        self.field.widget.upload_settings = self.get_settings()

    def get_urls(self):
        from django.conf.urls import patterns, url, include
        urlpatterns = patterns('',
            url(r'^(?P<key>%s)/upload/$' % self.key, self.upload, name='plupload-upload')
        )
        return urlpatterns

    def urls(self):
        return self.get_urls()
    urls = property(urls)

    def file_modify(self, file_absolute_path):
        file_path = os.path.relpath(file_absolute_path, settings.MEDIA_ROOT)
        file_url = os.path.join(settings.MEDIA_URL, file_path)
        return file_path, file_url

    def get_settings(self, *args, **kwargs):
        return dict(self.default_settings, **self.upload_settings)

    def get_upload_directory(self):
        directory = getattr(self.field, 'directory', None)
        if directory:
            return os.path.join(settings.UPLOAD_ROOT, directory)
        else:
            return settings.UPLOAD_ROOT

    def handle_uploaded_file(self, request, upload_directory):
        uploaded_file = request.FILES['file']
        chunk = request.REQUEST.get('chunk', '0')
        chunks = request.REQUEST.get('chunks', '0')
        name = request.REQUEST.get('name', '')
        if not name:
             name = uploaded_file.name
        local_file = os.path.join(upload_directory, name)
        with open(local_file, ('wb' if chunk == '0' else 'ab')) as f:
            for content in uploaded_file.chunks():
                f.write(content)
        if int(chunk) + 1 >= int(chunks):
            f.close()
            return local_file
        return None

    @method_decorator(require_POST)
    def upload(self, request, key=None):
        upload_directory = self.get_upload_directory()
        if (not os.path.exists(upload_directory)):
            os.makedirs(upload_directory)
        file_absolute_path = self.handle_uploaded_file(request,
            upload_directory=upload_directory)
        if not file_absolute_path:
            return HttpResponse(json.dumps({'chunk': True}), mimetype='application/json')
        try:
            file_path, file_url =  self.file_modify(file_absolute_path)
        except PluploadFileNotValid as error:
            return HttpResponse(json.dumps({'error': error.message}),
                                mimetype='application/json', status=200)
        response_data = {"url" : file_url, "path" : file_path}
        response_data["data"] = self.get_response_data(request, file_absolute_path)
        return self.get_response(request, response_data)

    def get_response_data(self, request, file_absolute_path):
        return None

    def get_response(self, request, response_data, **kwargs):
        response = HttpResponse(json.dumps(response_data), mimetype='application/json')
        response['Expires'] = 'Mon, 1 Jan 2000 01:00:00 GMT'
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
        response['Pragma'] = 'no-cache'
        return response
