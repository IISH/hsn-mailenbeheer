# -*- coding: utf-8 -*-

"""
Author:		Fons Laan, KNAW IISH - International Institute of Social History
Project:	HSN Mail
Name:		loginout/views.py
Version:	1.0.0
Goal:		Views for login & logout

Functions:
json_response( func )
def none2empty( var ):
login( request )

logout( request )

02-Mar-2016	Created
16-Mar-2016	Changed
"""

# python-future for Python 2/3 compatibility
from __future__ import ( absolute_import, division, print_function, unicode_literals )
from builtins import ( ascii, bytes, chr, dict, filter, hex, input, int, map, next, 
	oct, open, pow, range, round, str, super, zip )

from sys import stderr, exc_info
import os
import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from hsnmailenbeheer import settings
from qx.ldap_authenticate import ldap_authenticate


@csrf_exempt
def login( request ):
	print( "loginout/views/login()" )
	
#	scheme_authority, sub_site = get_server_info( request )

	template = "index.html"
	dictionary = \
	{
	#	'SUB_SITE'      : sub_site,
	#	'STATIC_PREFIX' : scheme_authority,
		'STATIC_PREFIX' : '',
	#	'STATIC_URL'    : settings.STATIC_URL,
	#	'STATIC_URL'    : '127.0.0.1',
		'STATIC_URL'    : '/',
	}

	# context contains csrf_token (and STATIC_URL for django >= 1.3)
#	context = context_instance = RequestContext( request )
	context = RequestContext( request )

	if request.method == "GET":
		REQUEST = request.GET
	else:
		REQUEST = request.POST
		
	username = REQUEST.get( "usr" )
	password = REQUEST.get( "pwd" )

	print( "username:", username )
	print( "password:", password )
	
	is_ldap_authenticated = ldap_authenticate( username, password )
	
	status = msg = ""
	if is_ldap_authenticated:
		print( "User: %s LDAP authenticated OK" % username )
		status = "ok"
		msg    = "LDAP Authentication OK"
		
		"""
		# now check local login
		is_hsn_authenticated, is_hsn_active = hsn_authenticate( username, password )
		print( "is_hsn_authenticated: %s, is_hsn_active: %s" % ( is_hsn_authenticated, is_hsn_active ) )
		
		if is_hsn_authenticated:
			if is_hsn_active:
				status = "ok"
				msg = "Hello %s" % username
			else:
				status = "HSN fail"
				msg = "HSN user <b>%s</b> is not active" % username
		else:
			status = "HSN fail"
			msg = "HSN user <b>%s</b> authentication failure" % username
		"""
	else:
		print( "User: %s NOT LDAP authenticated" % username )
		status = "LDAP fail"
		msg    = "LDAP Authentication failure"
	
	dictionary = \
	{
		"status"    : status,
		"msg"       : msg,
		"timestamp" : settings.TIMESTAMP_SERVER
	}

	return JsonResponse( dictionary )



def hsn_authenticate( username, password ):
	print( "loginout/views/hsn_authenticate()" )
	
	is_authenticated = False
	is_active = False
	
	user = authenticate( username = username, password = password )
	
	if user is not None:	# the password is verified for the user
		if user.is_active:
			is_authenticated = True
			is_active = True
			print( "User is valid, active and authenticated" )
			
			#c = Client()
			#c.login(username='fred', password='secret')

		else:
			is_authenticated = True
			print( "The password is valid, but the account has been disabled!" )
	else:
		# the authentication system was unable to verify the username and password
		print( "The username and password were incorrect." )

	return is_authenticated, is_active



@csrf_exempt
def logout( request ):
	print( "loginout/views/logout()" )
	
	if request.method == "GET":
		REQUEST = request.GET
	else:
		REQUEST = request.POST
		
	username = REQUEST.get( "usr" )
	
	dictionary = \
	{
		"status"    : "ok?",
		"msg"       : "User %s was logged off" % username,
	}

	return JsonResponse( dictionary )

# [eof]
