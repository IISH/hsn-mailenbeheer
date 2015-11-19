# -*- coding: utf-8 -*-

"""
Author:		Fons Laan, KNAW IISH - International Institute of Social History
Project:	HSN Mail
Name:		settings_local.py
Version:	0.1
Goal:		Django local settings sample for hsnmailenbeheer project

Use this file settings_local_sample.py as a template to create a file 
settings_local.py in the same directory. 
Uncomment the variables you need, and supply appropriate contents, for: 
	SECRET_KEY
	AUTH_LDAP_SERVER_URI
	AUTH_LDAP_USER_DN_TEMPLATE
	AUTH_LDAP_START_TLS
	DATABASES	USER & PASSWORD
	MAIL_PRINT_DIR
	MAIL_ADD_ID_IN_FN
	MAIL_SENT_TO_PRINTER
	MAIL_UPDATE_TABLE

17-Nov-2015	Created
17-Nov-2015	Changed
"""

# python-future for Python 2/3 compatibility
from __future__ import ( absolute_import, division, print_function, unicode_literals )
from builtins import ( ascii, bytes, chr, dict, filter, hex, input, int, map, next, 
	oct, open, pow, range, round, str, super, zip )

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
# Create a new SECRET_KEY with the command: 
# $ python -c 'import random; print "".join([random.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)") for i in range(50)])'
#SECRET_KEY = ''

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# local settings: db, etc

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
	'default': {
		'ENGINE'  : 'django.db.backends.mysql',
		'NAME'    : 'hsn_mail',
		'USER'    : '',
		'PASSWORD': '',
		'HOST'    : '127.0.0.1',
		'PORT'    : '3306',
	}
}

STATIC_ROOT = os.path.abspath( os.path.join( PROJECT_GRANNY, "static" ) )
print( "STATIC_ROOT:", STATIC_ROOT )

# LDAP authentication
AUTHENTICATION_BACKENDS = (
	'django_auth_ldap.backend.LDAPBackend',
#	'django.contrib.auth.backends.ModelBackend',	# needed? depends, see pyldap docs
)

AUTH_LDAP_SERVER_URI = ""
AUTH_LDAP_USER_DN_TEMPLATE = ""
AUTH_LDAP_START_TLS = True	# need secure connection? enable the StartTLS (preferred), or use ldaps:// URL

# django-registration; we only use the simple one-step workflow
REGISTRATION_OPEN = False	# false: no new accounts possible


# host used for cups querying for printers
#HOST = "localhost"
HOST = "127.0.0.1"

#MAIL_PRINT_DIR = "/home/fons/projects/python/Django/hsnmailenbeheer/hsnmailenbeheer/print"
MAIL_PRINT_DIR = "/tmp"

MAIL_ADD_ID_IN_FN    = True		# mail pk id in ps filename
MAIL_SENT_TO_PRINTER = False		# print the PostScript letter files
MAIL_UPDATE_TABLE    = False		# update status and print_date

print( "MAIL_PRINT_DIR:      ", MAIL_PRINT_DIR )
print( "MAIL_ADD_ID_IN_FN:   ", MAIL_ADD_ID_IN_FN )
print( "MAIL_SENT_TO_PRINTER;", MAIL_SENT_TO_PRINTER )
print( "MAIL_UPDATE_TABLE:   ", MAIL_UPDATE_TABLE )

CLEAR_CACHE_ON_RESTART = True
if CLEAR_CACHE_ON_RESTART:
	print( "Clearing Django cache", file = sys.stderr )
#	django.setup() # Needed to make django ready from the external script
	cache.clear()  # Flush all the old cache entries

# [eof]
