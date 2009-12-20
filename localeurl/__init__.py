# Copyright (c) 2008 Joost Cassee
# Licensed under the terms of the MIT License (see LICENSE.txt)

import re
from django.conf import settings

SUPPORTED_LOCALES = dict(settings.LANGUAGES)
LOCALES_RE = '|'.join(SUPPORTED_LOCALES)
PATH_RE = re.compile(r'^/(?P<locale>%s)(?P<path>.*)$' % LOCALES_RE)

LOCALE_INDEPENDENT_PATHS = getattr(settings, 'LOCALE_INDEPENDENT_PATHS', ())

LOCALE_INDEPENDENT_MEDIA_URL = getattr(settings,
        'LOCALE_INDEPENDENT_MEDIA_URL', True)

PREFIX_DEFAULT_LOCALE = getattr(settings, 'PREFIX_DEFAULT_LOCALE', True)
