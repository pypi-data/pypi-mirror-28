# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

# NOTE: https://stackoverflow.com/questions/8428556/django-default-settings-convention-for-pluggable-app


try:
    GITHUB_API_URL = getattr(settings, 'GITHUB_API_URL')
except AttributeError:
    raise ImproperlyConfigured("The GITHUB_API_URL setting must be set.")

try:
    GITHUB_ACCESS_TOKEN = getattr(settings, 'GITHUB_ACCESS_TOKEN')
except AttributeError:
    raise ImproperlyConfigured("The GITHUB_ACCESS_TOKEN setting must be set.")
