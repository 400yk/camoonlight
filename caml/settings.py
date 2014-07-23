"""
Django settings for caml project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
STATIC_ROOT = os.path.join(BASE_DIR, '../../caml_static').replace('\\','/')

SITE_ID = 2
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'v*089on$q#wm3h*f=m=yi8c-r3wa!gl-o8fvdo!&)^w42^_x=9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = True
LOGIN_REDIRECT_URL = '/'
ALLOWED_HOSTS = [
        '.camoonlight.com',
        '.camoonlight.com.',
        ]

# Tell Django about the profile object
AUTH_PROFILE_MODULE = "ca.UserProfile"

# Application definition

INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'bootstrapform',
        'haystack',
        'south',
        'ca',
        )

MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        )

ROOT_URLCONF = 'caml.urls'

WSGI_APPLICATION = 'caml.wsgi.application'

if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    os.environ['DJANGO_SETTINGS_MODULE'] = 'caml.settings'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'test_caml',
            'USER': 'youngwide',
            'PASSWORD': '198989',
            'HOST': 'localhost',
            'PORT': '3306',
            }
        }

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = 'http://www.camoonlight.com/ca/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'ca/media/').replace('\\','/')
MEDIA_URL = 'http://www.camoonlight.com/ca/media/'
LOGIN_URL = 'http://www.camoonlight.com/ca/login/'
"""
HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
            'URL': 'http://127.0.0.1:9200/',
            'INDEX_NAME': 'haystack',
            },
        }
"""
"""
HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
            'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
            },
        }
"""
HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
            'URL': 'http://127.0.0.1:8983/solr'
            },
        }

try:
    from settings_dev import *
except ImportError, e:
    pass
