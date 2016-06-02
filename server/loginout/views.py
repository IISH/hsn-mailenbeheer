# -*- coding: utf-8 -*-

"""
Author:		Fons Laan, KNAW IISH - International Institute of Social History
Project:	HSN Mail
Name:		loginout/views.py
Version:	1.0.0
Goal:		Views for login & logout

Functions:
def hsn_login( request ):
def hsn_authenticate( request, username, password ):
def hsn_logout( request ):

02-Mar-2016	Created
17-Mar-2016	@login_required added
02-Jun-2016	@csrf_exempt only for function hsn_login
02-Jun-2016	Changed
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
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from hsnmailenbeheer import settings
from .ldap_authenticate import ldap_authenticate


@csrf_exempt
def hsn_login( request ):
	print( "loginout/views/hsn_login()" )

	# 02-Jun-2016 with @csrf_exempt on this function, a csrftoken automatically 
	# shows up in firebug, after the cookies were manually removed. 

	# It seems that the browser automatically sends these cookies, so apparently I do not 
	# have to copy the csrftoken with qooxdoo in the client into subsequent request objects. 
	csrftoken = request.COOKIES.get( "csrftoken" )
	sessionid = request.COOKIES.get( "sessionid" )
	print( "csrftoken:", csrftoken )
	print( "sessionid:", sessionid )
	
	# context contains csrf_token (and STATIC_URL for django >= 1.3)
#	context = context_instance = RequestContext( request )
	context = RequestContext( request )
	
	if request.method == "GET":
		REQUEST = request.GET
	else:
		REQUEST = request.POST
	
	username = REQUEST.get( "usr" )
	password = REQUEST.get( "pwd" )

#	print( "username:", username )
#	print( "password:", password )
	
	if username is None or password is None:
		print( "User: %s NOT LDAP authenticated" % username )
		status = "LDAP fail"
		msg    = "LDAP Authentication failure for user %s" % username
	else:
		is_ldap_authenticated = ldap_authenticate( username, password )
		
		status = msg = ""
		if is_ldap_authenticated:
			print( "User: %s LDAP authenticated OK" % username )
			status = "ok"
			msg    = "LDAP Authentication OK"
			
			# now check local app login
			is_hsn_authenticated, is_hsn_active = hsn_authenticate( request, username, password )
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
			
		else:
			print( "User: %s NOT LDAP authenticated" % username )
			status = "LDAP fail"
			msg    = "LDAP Authentication failure for user %s" % username
	
	dictionary = \
	{
		"status"    : status,
		"msg"       : msg,
		"timestamp" : settings.TIMESTAMP_SERVER
	}

	return JsonResponse( dictionary )



def hsn_authenticate( request, username, password ):
	print( "loginout/views/hsn_authenticate()" )
	
	is_authenticated = False
	is_active = False
	
	user = authenticate( username = username, password = password )
	
	if user is not None:
		is_authenticated = True
		if user.is_active:
			is_active = True
			print( "User %s authenticated is active" % username )
		login( request, user )
	else:
		print( "login failed" )
	
	
	"""
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
	"""
	
	return is_authenticated, is_active



@login_required
def hsn_logout( request ):
	print( "loginout/views/hsn_logout()" )
	
	# Note that logout() doesn’t throw any errors if the user wasn’t logged in.
	logout( request )
	
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
