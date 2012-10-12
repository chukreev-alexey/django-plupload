# coding: utf-8

import os

from django.conf import settings

STATIC_URL = getattr(settings, "PLUPLOAD_STATIC_URL", settings.STATIC_URL)
MEDIA_ROOT = getattr(settings, "PLUPLOAD_MEDIA_ROOT", settings.MEDIA_ROOT)
MEDIA_URL = getattr(settings, "PLUPLOAD_MEDIA_URL", settings.MEDIA_URL)
UPLOAD_ROOT = getattr(settings, "PLUPLOAD_UPLOAD_ROOT", os.path.join(MEDIA_ROOT, 'uploads/'))