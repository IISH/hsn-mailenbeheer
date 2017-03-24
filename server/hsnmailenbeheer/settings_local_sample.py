# -*- coding: utf-8 -*-

"""
Author:		Fons Laan, KNAW IISH - International Institute of Social History
Project:	HSN Mail
Name:		settings_local.py
Version:	1.0.1
Goal:		Django local settings for hsnmail project

22-Mar-2016	Created
20-Mar-2017	Changed
"""

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
SECRET_KEY = ''	# put your secret key here

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ADMIN_ENABLED = DEBUG

ALLOWED_HOSTS = [ 'localhost' ]		# not empty when DEBUG = False


# Database
#https://docs.djangoproject.com/en/1.9/topics/db/multi-db/
"""
DATABASES = {
	'default': {
		'NAME'    : 'hsn_django',
		'ENGINE'  : 'django.db.backends.mysql',
		'USER'    : '<db_user>',
		'PASSWORD': '<db_pwd>',
		'HOST'    : '<db_host>',
		'PORT'    : '<db_port>',
	}
},
	'mail': {
		'NAME'    : 'hsn_mail',
		'ENGINE'  : 'django.db.backends.mysql',
		'USER'    : '<db_user>',
		'PASSWORD': '<db_pwd>',
		'HOST'    : '<db_host>',
		'PORT'    : '<db_port>',
	}
},
	'central': {
		'NAME'    : 'hsn_central',
		'ENGINE'  : 'django.db.backends.mysql',
		'USER'    : '<db_user>',
		'PASSWORD': '<db_pwd>',
		'HOST'    : '<db_host>',
		'PORT'    : '<db_port>',
	}
},
	'reference': {
		'NAME'    : 'hsn_reference',
		'ENGINE'  : 'django.db.backends.mysql',
		'USER'    : '<db_user>',
		'PASSWORD': '<db_pwd>',
		'HOST'    : '<db_host>',
		'PORT'    : '<db_port>',
	}
}
"""

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
#LDAP_SEARCH_USERNAME = "<your_ldap_search_username>"
#LDAP_SEARCH_PASSWORD = "<your_ldap_search_password>"
# for testing
#LDAP_TEST_USERNAME = "<your_ldap_test_username>"
#LDAP_TEST_PASSWORD = "<your_ldap_test_password>"

LDAP_URI = "<your_ldap_uri>"
DC_HOST  = "<your_dc_host>"


CLEAR_CACHE_ON_RESTART = True
if CLEAR_CACHE_ON_RESTART:
	print( "Clearing Django cache", file = sys.stderr )
#	django.setup() # Needed to make django ready from the external script
	cache.clear()  # Flush all the old cache entries

# [eof]
