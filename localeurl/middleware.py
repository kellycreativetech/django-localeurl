# Copyright (c) 2008 Joost Cassee
# Licensed under the terms of the MIT License (see LICENSE.txt)

import re
from django import http
from django.conf import settings
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from django.utils import translation
import localeurl
from localeurl import utils

# Make sure the default language is in the list of supported languages
assert utils.supported_language(settings.LANGUAGE_CODE) is not None, \
        "Please ensure that settings.LANGUAGE_CODE is in settings.LANGUAGES."

class LocaleURLMiddleware(object):
    """
    Middleware that sets the language based on the request path prefix and
    strips that prefix from the path. It will also automatically redirect any
    path without a prefix, unless PREFIX_DEFAULT_LOCALE is set to True.
    Exceptions are paths beginning with MEDIA_URL or matching any regular
    expression from LOCALE_INDEPENDENT_PATHS from the project settings.

    For example, the path '/en/admin/' will set request.LANGUAGE_CODE to 'en'
    and request.path to '/admin/'.

    Alternatively, the language is set by the first component of the domain
    name. For example, a request on 'fr.example.com' would set the language to
    French.

    If you use this middleware the django.core.urlresolvers.reverse function
    is be patched to return paths with locale prefix (see models.py).
    """
    def process_request(self, request):
        locale, path = self.split_locale_from_request(request)
        locale_path = utils.locale_path(path, locale)
        if locale_path != request.path_info:
            return HttpResponseRedirect(locale_path)
        request.path_info = path
        if not locale:
            locale = settings.LANGUAGE_CODE
        translation.activate(locale)
        request.LANGUAGE_CODE = translation.get_language()

    def process_response(self, request, response):
        if 'Content-Language' not in response:
            response['Content-Language'] = translation.get_language()
        translation.deactivate()
        return response

    def split_locale_from_request(self, request):
        if localeurl.settings.URL_TYPE == 'domain_prefix':
            locale, _ = utils.strip_domain(request.get_host())
            path_info = request.path_info
        else:
            locale, path_info = utils.strip_path(request.path_info)
        return locale, path_info
