# -*- coding: utf-8 -*-

"""
Author:		Fons Laan, KNAW IISH - International Institute of Social History
Project:	HSN Mail
Name:		views.py
Version:	1.0.0
Goal:		View for op_select

Functions:
json_response( func )
def none2empty( var ):
login( request )
gethsndata( request )
gethsnopdata( request )
puthsnmanage( request )
puthsnmanagemissing( request )
putmailbev( request )
putmailhuw( request )
putmailbevreceived( request )
putopmutation( request )
printmailbev( request )

22-Jun-2015	Created
24-Feb-2016	Changed
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
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from hsnmailenbeheer import settings
from hsn_manage.views import ( get_marriages, get_deaths, get_partners, get_missing, get_hsnmanage, 
	put_hsnmanage, put_hsnmanagemissing )
from mail.views import ( get_locations, get_municipalities, get_sources, get_text_strings, 
	get_mails, get_mails_print, 
	put_mailbev, put_mailhuw, put_mailbevreceived, put_opmutation )
from mail.print import print_mailbev
from op_select.op import get_op_info
from mail.cupstree import get_printers


def json_response( func ):
	"""
	A decorator thats takes a view response and turns it
	into json. If a callback is added through GET or POST
	the response is JSONP.
	"""
	def decorator( request, *args, **kwargs ):
		objects = func( request, *args, **kwargs )
		if isinstance( objects, HttpResponse ):
			return objects
		try:
			data = simplejson.dumps( objects )
			if 'callback' in request.REQUEST:
				# a jsonp response!
				data = '%s(%s);' % ( request.REQUEST[ 'callback' ], data )
				return HttpResponse( data, "text/javascript" )
		except:
			data = simplejson.dumps( str( objects ) )
		return HttpResponse( data, "application/json" )
	return decorator



def none2empty( var ):
	if var == None: 
		var = ""
	return var



@csrf_exempt
def login( request ):
	print( "qx/views/login()" )
	
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

#	return render_to_response( template, dictionary, context )
#	return render( template, dictionary, context )
#	return render( dictionary, context )
#	return HttpResponse( "Hello, world. You're at qx login." )

	dictionary = \
	{
		"status"    : "ok",
		"timestamp" : settings.TIMESTAMP_SERVER,
		"msg"       : "Hello, world. You're at qx login."
	}

	return JsonResponse( dictionary )



@csrf_exempt
#@login_required
def gethsndata( request ):
	print( "qx/views/gethsndata()" )

	# Notice: in the client we only use locations (Plaats), 
	# never municipalities (Gemeente), even if the GUI says Gemeente. 
	# Municipality can be used in the Mail letters
	
	printers       = get_printers()
	locations      = get_locations()
#	municipalities = get_municipalities()
	sources        = get_sources()
	strings        = get_text_strings()
	mails_print    = get_mails_print()
	
	dictionary = \
	{
		"timestamp_server" : settings.TIMESTAMP_SERVER,
		"printers"         : printers,
		"locations"        : locations,
	#	"municipalities"   : municipalities,	# not needed in client, only for letter printing
		"sources"          : sources,
		"strings"          : strings,
		"mails_print"      : mails_print
	}
	
	return JsonResponse( dictionary )



@csrf_exempt
def gethsnopdata( request ):
	print( "qx/views/gethsnopdata() %s %s" % ( request.scheme, request.method ) )
	
	if request.method == "GET":
		REQUEST = request.GET
	else:
		REQUEST = request.POST
		
#	op_number = request.POST.get( "op_num" )
	op_number = REQUEST.get( "op_num" )
	
	op_err_str = ""
	op_info_list = get_op_info( op_number )
	if len( op_info_list ) == 0:
		op_err_str = "Geen OP gevonden voor OP-nummer %s" % op_number
		op_isvalid = False
	else:
		op_isvalid = True
	print( "op_isvalid: ", op_isvalid )
	
	for op_info_dict in op_info_list:
		print( "op_info_dict:", op_info_dict )
	
	marriages = {}
	missing_data = {}
	hsnmanage = { "statustekst" : "" }
	partners = {}
	mails = {}
	deaths = {}
	
	if op_isvalid:
		marriages = get_marriages( op_number )
		print( "marriages: ", marriages )
	
		missing_data = get_missing( op_number )
		print( "missing data: ", missing_data )
	
		hsnmanage = get_hsnmanage( op_number )
		print( "hsnmanage: ", hsnmanage )
	
		partners = get_partners( op_number )
		print( "partners: ", partners )
	
		mails = get_mails( op_number )
		print( "mails: ", mails )
	
		deaths = get_deaths( op_number )
		print( "deaths: ", deaths )
		
		# sometimes the death location is not [yet] present in the HsnBeheer table, 
		# but we [sometimes] can display it from the Ovlknd table
		if hsnmanage.get( "ovlplaats" ) == "":
			for death in deaths:
				if death.get( "table_name" ) == "Ovlknd":
					hsnmanage[ "ovlplaats" ] = death.get( "death_location" )
		
	OP = \
	{
		"op_num"       : op_number,
		"op_err_str"   : op_err_str,
		"op_info_list" : op_info_list,
		
		"hsnmanage"    : hsnmanage,
		"marriages"    : marriages,
		"missing_data" : missing_data,
		"partners"     : partners,
		"mails"        : mails,
		"deaths"       : deaths
	}
		
	dictionary = \
	{
		"op_isvalid" : op_isvalid,
		"OP" : OP
	}
	

	"""	
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

	context = RequestContext( request )
		
#	json_data = json.dumps( dictionary )
#	content_type = "application/json; charset=UTF-8"
#	return HttpResponse( json_data, content_type )
#	return render_to_response( template, dictionary, context )
#	return render( json_data, content_type, context )
	"""
	
	return JsonResponse( dictionary )



@csrf_exempt
def puthsnmanage( request ):
	print( "qx/views/puthsnmanage()" )

	if request.method == "GET":
		REQUEST = request.GET
	else:
		REQUEST = request.POST

	ovldag  = REQUEST.get( "death_day" )
	ovlmnd  = REQUEST.get( "death_month" )
	ovljaar = REQUEST.get( "death_year" )
	
	if not ovldag:  ovldag  = 0		# declared int in db
	if not ovlmnd:  ovlmnd  = 0		# declared int in db
	if not ovljaar: ovljaar = 0		# declared int in db
		
	fields = {
		"idnr"      : int( REQUEST.get( "op_num" ) ),
		"ovldag"    : ovldag,
		"ovlmnd"    : ovlmnd,
		"ovljaar"   : ovljaar,
		"ovlplaats" : REQUEST.get( "death_location" ),
		"fase_a"    : REQUEST.get( "phase_a" ),
		"fase_b"    : REQUEST.get( "phase_b" ),
		"fase_c_d"  : REQUEST.get( "phase_cd" )
	}
	
	
	
	# the remaining 3 fields: invoerstatus, randomgetal, releasestatus 
	# are left unchanged (their values are not  in the request data). 
	
	status = put_hsnmanage( fields )

	return JsonResponse( { "status" : status } )



@csrf_exempt
def puthsnmanagemissing( request ):
	print( "qx/views/puthsnmanagemissing()" )

	if request.method == "GET":
		REQUEST = request.GET
	else:
		REQUEST = request.POST

	missing_str = REQUEST.get( "missing" );
	missing = json.loads( missing_str )
#	print( missing )

	status, msg = put_hsnmanagemissing( missing )

	return JsonResponse( { "status" : status, "msg" : msg } )



@csrf_exempt
def putmailbev( request ):
	print( "qx/views/putmailbev()" )

	if request.method == "GET":
		REQUEST = request.GET
	else:
		REQUEST = request.POST

	mailbev_str = REQUEST.get( "mailbev" );
	if mailbev_str is None:
		status = "ERROR"
		msg = "No JSON"
		return JsonResponse( { "status" : status, "msg" : msg } )
	
	mailbev = json.loads( mailbev_str )
#	print( mailbev )

	status, msg = put_mailbev( mailbev )

	return JsonResponse( { "status" : status, "msg" : msg } )



@csrf_exempt
def putmailhuw( request ):
	print( "qx/views/putmailhuw()" )

	if request.method == "GET":
		REQUEST = request.GET
	else:
		REQUEST = request.POST

	mailhuw_str = REQUEST.get( "mailhuw" );
	if mailhuw_str is None:
		status = "ERROR"
		msg = "No JSON"
		return JsonResponse( { "status" : status, "msg" : msg } )

	mailhuw = json.loads( mailhuw_str )
#	print( mailhuw )

	status, msg = put_mailhuw( mailhuw )

	return JsonResponse( { "status" : status, "msg" : msg } )



@csrf_exempt
def putmailbevreceived( request ):
	print( "qx/views/putmailbevreceived()" )

	if request.method == "GET":
		REQUEST = request.GET
	else:
		REQUEST = request.POST
		
	mailbevreceived_str = REQUEST.get( "mailbevreceived" );
	if mailbevreceived_str is None:
		status = "ERROR"
		msg = "No JSON"
		return JsonResponse( { "status" : status, "msg" : msg } )

	mailbevreceived = json.loads( mailbevreceived_str )
	print( mailbevreceived )

	status, msg = put_mailbevreceived( mailbevreceived )

	return JsonResponse( { "status" : status, "msg" : msg } )



@csrf_exempt
def putopmutation( request ):
	print( "qx/views/putopmutation()" )

	if request.method == "GET":
		REQUEST = request.GET
	else:
		REQUEST = request.POST

	opmutation_str = REQUEST.get( "opmutation" );
	if opmutation_str is None:
		status = "ERROR"
		msg = "No JSON"
		return JsonResponse( { "status" : status, "msg" : msg } )

	opmutation = json.loads( opmutation_str )
	print( opmutation )
	
	status, msg = put_opmutation( opmutation )

	return JsonResponse( { "status" : status, "msg" : msg } )



@csrf_exempt
def printmailbev( request ):
	print( "qx/views/printmailbev()" )
	
	# no parameters; all mails with type = "BEV" + status = 0 will be printed
	# status will be updated from 0 to 1
	status, msg, ids = print_mailbev()
	
	return JsonResponse( { "status" : status, "msg" : msg, "ids" : ids } )

# [eof]
