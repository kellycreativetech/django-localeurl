"""
Test settings.
"""

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = ':memory:'

SITE_ID = 1

ROOT_URLCONF = 'localeurl.tests.test_urls'

INSTALLED_APPS = (
    'localeurl',
)
