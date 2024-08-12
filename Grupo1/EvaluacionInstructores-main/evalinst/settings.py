import os
import json
from pathlib import Path
from urllib.parse import quote_plus
import smtplib

with open('D:/json_config/evalinstructorV1.json') as config_file:
    config = json.load(config_file)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = config['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #Aplicaciones
    'evalinst',
    'loadlist',
    'administracion',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    #otros middleware
    #'administracion.middleware.TimeBasedAccessMiddleware'
]

ROOT_URLCONF = 'evalinst.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'evalinst.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, "dbs/evalinst.db"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Bogota'
# DATETIME_FORMAT = '%d-%m-%Y %H:%M:%S' 
USE_I18N = True
USE_L10N = True
USE_TZ = True


# PRODUCTION
LOGIN_URL= '/loginPage'
STATIC_ROOT = os.path.join(BASE_DIR, "/static/")
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
# smtp server port if TLS = 587, or SSL = 465
EMAIL_HOST_USER = config['EMAIL_USER']
EMAIL_HOST_PASSWORD = config['EMAIL_PASSWORD']


MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = '/media/'

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 3600 # in seconds
SESSION_COOKIE_SAMESITE = None
SESSION_COOKIE_SECURE = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = False
SECURE_HSTS_PRELOAD = True
X_FRAME_OPTIONS = 'SAMEORIGIN'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
