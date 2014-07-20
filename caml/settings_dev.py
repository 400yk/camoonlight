DEBUG = True
TEMPLATE_DEBUT = True

COMPRESS_AUTO = True
SESSION_COOKIE_SECURE = True

ALLOWED_HOSTS = []
STATIC_URL = '/static/'

SITE_ID = 3

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test_caml',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '3306',
        }
    }

