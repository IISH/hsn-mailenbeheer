# future-0.16.0 imports for Python 2/3 compatibility
from __future__ import ( absolute_import, division, print_function, unicode_literals )
from builtins import ( ascii, bytes, chr, dict, filter, hex, input, int, list, map, 
    next, object, oct, open, pow, range, round, super, str, zip )

import os
import sys

import django
from django.core.cache import cache


PROJECT_ROOT   = os.path.abspath( os.path.dirname( __file__ ) )
PROJECT_PARENT = os.path.dirname( PROJECT_ROOT )
PROJECT_GRANNY = os.path.dirname( PROJECT_PARENT )
print( "PROJECT_ROOT:", PROJECT_ROOT )
print( "PROJECT_PARENT:", PROJECT_PARENT )
print( "PROJECT_GRANNY:", PROJECT_GRANNY )


# SECURITY WARNING: keep the secret key used in production secret!
# create a new SECRET_KEY with (requires django_extensions package): 
# $ python manage.py generate_secret_key
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ADMIN_ENABLED = DEBUG

ALLOWED_HOSTS = [ '*' ]		# not empty when DEBUG = False


# Database
#https://docs.djangoproject.com/en/1.9/topics/db/multi-db/
DATABASES = {
	'default': {
		'NAME'    : 'hsn_django',
		'ENGINE'  : 'django.db.backends.mysql',
		'USER'    : os.environ.get('DB_DJANGO_USER'),
		'PASSWORD': os.environ.get('DB_DJANGO_PASSWORD'),
		'HOST'    : os.environ.get('DB_DJANGO_HOST'),
		'PORT'    : os.environ.get('DB_DJANGO_PORT'),
	},
	'mail': {
		'NAME'    : 'hsn_mail',
		'ENGINE'  : 'django.db.backends.mysql',
		'USER'    : os.environ.get('DB_MAIL_USER'),
		'PASSWORD': os.environ.get('DB_MAIL_PASSWORD'),
		'HOST'    : os.environ.get('DB_MAIL_HOST'),
		'PORT'    : os.environ.get('DB_MAIL_PORT'),
	},
	'central': {
		'NAME'    : 'hsn_central',
		'ENGINE'  : 'django.db.backends.mysql',
		'USER'    : os.environ.get('DB_CENTRAL_USER'),
		'PASSWORD': os.environ.get('DB_CENTRAL_PASSWORD'),
		'HOST'    : os.environ.get('DB_CENTRAL_HOST'),
		'PORT'    : os.environ.get('DB_CENTRAL_PORT'),
	},
	'reference': {
		'NAME'    : 'hsn_reference',
		'ENGINE'  : 'django.db.backends.mysql',
		'USER'    : os.environ.get('DB_REFERENCE_USER'),
		'PASSWORD': os.environ.get('DB_REFERENCE_PASSWORD'),
		'HOST'    : os.environ.get('DB_REFERENCE_HOST'),
		'PORT'    : os.environ.get('DB_REFERENCE_PORT'),
	}
}

STATIC_ROOT = os.path.abspath( os.path.join( PROJECT_GRANNY, "static" ) )
print( "STATIC_ROOT:", STATIC_ROOT )

# django-registration; we only use the simple one-step workflow
REGISTRATION_OPEN = False	# False: no new accounts possible

# Printing stuff
# host used for querying for printers
#HOST = "localhost"
HOST = "127.0.0.1"

MAIL_PRINT_DIR = "/tmp"

MAIL_ADD_ID_IN_FN    = True		# mail pk id in ps filename
MAIL_SENT_TO_PRINTER = False		# print the PostScript letter files
MAIL_UPDATE_TABLE    = False		# update status and print_date

print( "MAIL_PRINT_DIR:      ", MAIL_PRINT_DIR )
print( "MAIL_ADD_ID_IN_FN:   ", MAIL_ADD_ID_IN_FN )
print( "MAIL_SENT_TO_PRINTER;", MAIL_SENT_TO_PRINTER )
print( "MAIL_UPDATE_TABLE:   ", MAIL_UPDATE_TABLE )

# IISG LDAP
# for LDAP search
if os.environ.get('LDAP_USERNAME') is not None and os.environ.get('LDAP_PASSWORD') is not None:
	LDAP_SEARCH_USERNAME = os.environ.get('LDAP_USERNAME')
	LDAP_SEARCH_PASSWORD = os.environ.get('LDAP_PASSWORD')

LDAP_URI = os.environ.get('LDAP_URI')
DC_HOST  = os.environ.get('DC_HOST')


CLEAR_CACHE_ON_RESTART = True
if CLEAR_CACHE_ON_RESTART:
	print( "Clearing Django cache", file = sys.stderr )
#	django.setup() # Needed to make django ready from the external script
	cache.clear()  # Flush all the old cache entries
