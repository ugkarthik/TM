"""
Django settings for trendzmania project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

from oscar import get_core_apps, OSCAR_MAIN_TEMPLATE_DIR
from oscar.defaults import *

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

location = lambda f_name: os.path.join(BASE_DIR, f_name)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'atl_tt#67r93n$%=11sbetx9)4#77e_jqw35lr5y%=t)+n14sy'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['trendzmania']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'compressor',
] + get_core_apps()

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.request",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'oscar.apps.search.context_processors.search_form',
    'oscar.apps.promotions.context_processors.promotions',
    'oscar.apps.checkout.context_processors.checkout',
    'oscar.apps.customer.notifications.context_processors.notifications',
    'oscar.core.context_processors.metadata',
    #'trendzmania.tm'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'oscar.apps.basket.middleware.BasketMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'trendzmania.urls'

WSGI_APPLICATION = 'trendzmania.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'trendzmania',
        'USER': 'trendzmania',
        'PASSWORD': '',
        'HOST': '',
        'ATOMIC_REQUESTS': True,
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


MEDIA_ROOT = location("media")

MEDIA_URL = '/media/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = location('static')

STATICFILES_DIRS = (
    location('public/static'),
)

TEMPLATE_DIRS = (
    location('templates'),
    OSCAR_MAIN_TEMPLATE_DIR,
)

AUTHENTICATION_BACKENDS = (
    'oscar.apps.customer.auth_backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Haystack settings - we use a local Solr instance running on the default port
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://127.0.0.1:8983/solr',
        'INCLUDE_SPELLING': True,
    },
}

SITE_ID = 1

try:
    from local_settings import *
except ImportError:
    pass