# -*- coding: utf-8 -*-
import os
from django import forms
from django.conf import settings
from sorl.thumbnail import get_thumbnail

from .sites import plupload_register
from .options import PluploadInstance
from .fields import PluploadFormField
from .widgets import PluploadWidget

class UploadForm(forms.Form):
    file1 = PluploadFormField(directory='exchange',
        widget=PluploadWidget(attrs={'class': 'grey_bt', 'value': 'Загрузить файл'})
    )
    file2 = PluploadFormField()

class File1Plupload(PluploadInstance):
    upload_settings = {
        "filters": [
            {"title": u"XML files", "extensions": "xml"}
        ]
    }

class File2Plupload(PluploadInstance):
    upload_settings = {
        "filters": [
            {"title": u"Images", "extensions": "jpg,png,gif"}
        ]
    }
    def file_modify(self, file_absolute_path):
        im = get_thumbnail(file_absolute_path, 'x130', upscale=False, quality=99)
        file_url = im.url
        file_path = os.path.relpath(file_absolute_path, settings.MEDIA_ROOT)
        return file_url, file_path

plupload_register.register((UploadForm, 'file1'), File1Plupload)
plupload_register.register((UploadForm, 'file2'), File2Plupload)
