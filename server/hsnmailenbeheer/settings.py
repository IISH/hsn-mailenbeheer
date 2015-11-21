# -*- coding: utf-8 -*-

"""
Author:		Fons Laan, KNAW IISH - International Institute of Social History
Project:	HSN Mail
Name:		settings.py
Version:	1.0.0
Goal:		Django settings for hsnmailenbeheer project

26-May-2015	Created
17-Nov-2015	Changed
"""

# python-future for Python 2/3 compatibility
from __future__ import (absolute_import, division, print_function, unicode_literals)
from builtins import (ascii, bytes, chr, dict, filter, hex, input, int, map, next,
                      oct, open, pow, range, round, str, super, zip)

import os
import sys

from django import get_version

TIMESTAMP_SERVER = "17-Nov-2015 11:54"

django_version_str = get_version()
django_version_lst = django_version_str.split('.')
DJANGO_MAJ_MIN = float(django_version_lst[0] + '.' + django_version_lst[1])  # ignore [2] = rev
print("Django version: %s" % DJANGO_MAJ_MIN, file=sys.stderr)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT   = os.path.abspath( os.path.dirname( __file__ ) )
PROJECT_PARENT = os.path.dirname( PROJECT_ROOT )
PROJECT_GRANNY = os.path.dirname( PROJECT_PARENT )
STATIC_ROOT = os.path.abspath( os.path.join( PROJECT_GRANNY, "static" ) )
print( "STATIC_ROOT:", STATIC_ROOT )
print( "PROJECT_ROOT:", PROJECT_ROOT )
print( "PROJECT_PARENT:", PROJECT_PARENT )
print( "PROJECT_GRANNY:", PROJECT_GRANNY )


# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'not_secret'  # must be overwritten in settings_local

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False  # can be overwritten in settings_local

ADMIN_ENABLED = DEBUG

ALLOWED_HOSTS = []  # overwritten in settings_local


# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 'debug_toolbar',
    'mail',
    'qx',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',  # not in Django-1.4.20
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',  # not in Django-1.4.20
)

ROOT_URLCONF = 'hsnmailenbeheer.urls'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',  # needed by django_tables2
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['qx'],
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

WSGI_APPLICATION = 'hsnmailenbeheer.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
# -> in settings_local
'''
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	}
}
'''

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/
LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Europe/Amsterdam'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

#LOGIN_URL = "login"
LOGIN_URL = "/accounts/login/"

HSN_START_DATE = 1811

# local settings: db, ...
hsn_mailenbeheer_home = os.environ.get('HSN_MAILENBEHEER_HOME')
if hsn_mailenbeheer_home:
    custom = hsn_mailenbeheer_home + '/settings.py'
    try:
        from custom import *
    except ImportError:
        print("Unable to find or parse the config file from {}".format(custom), file=sys.stderr)
        pass

# [eof]
