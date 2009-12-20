# Copyright (c) 2008 Joost Cassee
# Licensed under the terms of the MIT License (see LICENSE.txt)

from django.conf import settings
from django.core import urlresolvers
from django.core import urlresolvers
import localeurl

def is_locale_independent(path):
    """
    Returns whether the path is locale-independent.
    """
    if localeurl.LOCALE_INDEPENDENT_MEDIA_URL and settings.MEDIA_URL \
            and path.startswith(settings.MEDIA_URL):
        return True
    for regex in localeurl.LOCALE_INDEPENDENT_PATHS:
        if regex.search(path):
            return True
    return False

def strip_path(path):
    """
    Separates the locale prefix from the rest of the path. If the path does not
    begin with a locale it is returned without change.
    """
    check = localeurl.PATH_RE.match(path)
    if check:
        path_info = check.group('path') or '/'
        if path_info.startswith('/'):
            return check.group('locale'), path_info
    return '', path

def supported_language(locale):
    """
    Returns the supported language (from settings.LANGUAGES) for the locale.
    """
    if locale in localeurl.SUPPORTED_LOCALES:
        return locale
    elif locale[:2] in localeurl.SUPPORTED_LOCALES:
        return locale[:2]
    else:
        return None

def is_default_locale(locale):
    """
    Returns whether the locale is the default locale.
    """
    return locale == supported_language(settings.LANGUAGE_CODE)

def locale_path(path, locale=''):
    """
    Generate the localeurl-enabled path from a path without locale prefix. If
    the locale is empty settings.LANGUAGE_CODE is used.
    """
    locale = supported_language(locale)
    if not locale:
        locale = supported_language(settings.LANGUAGE_CODE)
    if is_locale_independent(path):
        return path
    elif is_default_locale(locale) and not localeurl.PREFIX_DEFAULT_LOCALE:
        return path
    else:
        return ''.join([u'/', locale, path])

def locale_url(path, locale=''):
    """
    Generate the localeurl-enabled URL from a path without locale prefix. If
    the locale is empty settings.LANGUAGE_CODE is used.
    """
    path = locale_path(path, locale)
    return ''.join([urlresolvers.get_script_prefix(), path[1:]])

def strip_script_prefix(url):
    """
    Strips the SCRIPT_PREFIX from the URL. Because this function is meant for
    use in templates, it assumes the URL starts with the prefix.
    """
    assert url.startswith(urlresolvers.get_script_prefix()), \
            "URL must start with SCRIPT_PREFIX: %s" % url
    pos = len(urlresolvers.get_script_prefix()) - 1
    return url[:pos], url[pos:]
