#!/usr/bin/env python

"""
Author:		Fons Laan, KNAW IISH - International Institute of Social History
Project:	HSN Mail
Name:		qx/ldap_authenticate.py
Version:	1.0.0
Goal:		LDAP authentication


see: https://www.python-ldap.org/doc/html/ldap.html

LDAP abbreviations:
	CN = Common Name
	OU = Organizational Unit
	DC = Domain Component
	
Sending LDAP requests: 
Most methods on LDAP objects initiate an asynchronous request to the LDAP server
and return a message id that can be used later to retrieve the result with result().

LDAP Methods with names ending in _s are the synchronous form and wait for and 
return with the server's result, or with None if no data is expected.

01-Mar-2016	Created
16-Mar-2016	Changed
"""

import sys
import collections
import ldap

from hsnmailenbeheer import settings
#from openldap_passwd import check_password		# no longer used


#debug = True
debug = settings.DEBUG

#LDAP_PORT = 389		# = default

try:
	LDAP_SEARCH_USERNAME = settings.LDAP_SEARCH_USERNAME
	LDAP_SEARCH_PASSWORD = settings.LDAP_SEARCH_PASSWORD
except:
	LDAP_SEARCH_USERNAME = ""
	LDAP_SEARCH_PASSWORD = ""
	
LDAP_URI = settings.LDAP_URI
DC_HOST  = settings.DC_HOST

DN_BASE   = "ou=users,%s" % DC_HOST
DN_SEARCH = "cn=%s,%s" % ( LDAP_SEARCH_USERNAME, DC_HOST )


def show_dict( ldap_dict ):
	if type( ldap_dict ) == dict:
		for( k, v ) in ldap_dict.iteritems():
			print( "%s: %s" % (k, v) )
	else:
		print( type( ldap_dict ) )
		print( ldap_dict )



def show_resp( resp ):
	if isinstance( resp, collections.Iterable):
		for iter0 in resp:
			if isinstance( iter0, collections.Iterable):
				for iter1 in iter0:
					if type( iter1 ) == dict:
						show_dict( iter1 )
					else:
					#	print( type( iter1 ) )
						print( iter1 )
			else:
				print( type( iter0 ) )
				print( iter0 )
	else:
		print( type( resp ) )
		print( resp )



def get_usr_dict( ldap_resp ):
	user_dict = None
	
	if isinstance( ldap_resp, collections.Iterable):
		for iter0 in ldap_resp:
			if isinstance( iter0, collections.Iterable):
				for iter1 in iter0:
					if type( iter1 ) == dict:
						user_dict = iter1
						break
	
	return user_dict



def find_user( ldap_client, username ):
	print( "\nfind_user()" )
	
	user_dict = None
	
	# bind admin to the server
	print( "ldap_client.simple_bind_s()" )
	print( "DN_SEARCH: %s" % DN_SEARCH )
	print( "LDAP_SEARCH_PASSWORD: %s" %  LDAP_SEARCH_PASSWORD )
	ldap_client.simple_bind_s( DN_SEARCH, LDAP_SEARCH_PASSWORD )

	# search user
	search_filter = "cn=%s" % username
	print( "ldap_client.search_s()" )
	print( "DN_BASE: %s" % DN_BASE )
	print( "ldap.SCOPE_SUBTREE: %s" % ldap.SCOPE_SUBTREE )
	print( "search_filter: %s" % search_filter )
	ldap_resp = ldap_client.search_s( DN_BASE, ldap.SCOPE_SUBTREE, search_filter )
	user_dict = get_usr_dict( ldap_resp )
	
	if user_dict is not None:
		is_user = True
		if debug:
			print( type( ldap_resp ), ldap_resp )
			print( "\nLDAP Search user:")
			show_resp( ldap_resp )
	
	return user_dict



def authenticate_remote( ldap_client, username, password ):
	print( "\nauthenticate_remote()" )
	
	dn_user = "cn=%s,ou=users,%s" % ( username, DC_HOST )
	
	print( "ldap_client.simple_bind_s()" )
	print( "dn_user: %s" % dn_user )
	print( "password: %s" % password )

	is_authenticated = True
	try:
		# bind user to the server
		ldap_client.simple_bind_s( dn_user, password )
	except ldap.INVALID_CREDENTIALS:
		print( "ldap.INVALID_CREDENTIALS" )
		print( "dn_user: %s" % dn_user )
		print( "password: %s" % password )
		is_authenticated = False
	
	return is_authenticated



def ldap_authenticate( username, password ):
	if debug:
		print( "ldap_authenticate()" )
		print( "LDAP_SEARCH_USERNAME: %s" % LDAP_SEARCH_USERNAME )
		print( "LDAP_SEARCH_PASSWORD: %s" % LDAP_SEARCH_PASSWORD )
		print( "LDAP_USER_USERNAME:  %s" % username )
		print( "LDAP_USER_PASSWORD:  %s" % password )
		print( "" )
		print( "LDAP_URI:  %s" % LDAP_URI )
		print( "DC_HOST:   %s" % DC_HOST )
		print( "DN_BASE:   %s" % DN_BASE )
		print( "DN_SEARCH: %s" % DN_SEARCH )
		print( "" )
	
	ldap_client = None
	is_authenticated = False
	
	try:
		ldap_client = ldap.initialize( LDAP_URI, trace_level = 0 )
		ldap_client.set_option( ldap.OPT_REFERRALS, 0 )
		ldap_client.set_option( ldap.OPT_PROTOCOL_VERSION, 3 )
		
		if not ( LDAP_SEARCH_USERNAME == "" or LDAP_SEARCH_PASSWORD == "" ):
			user_dict = find_user( ldap_client, username )
			#print( "user_dict: ", user_dict )
		
			if user_dict is not None:
				is_authenticated = authenticate_remote( ldap_client, username, password )
			
				"""
				# "local" authenticate no longer used
				ldap_uid = user_dict.get( "uid" )[ 0 ]
				tagged_digest_salt = user_dict.get( "userPassword" )[ 0 ]
				
				if debug: 
					print( "ldap uid: %s" % ldap_uid )
					print( "ldap_pwd: %s" % tagged_digest_salt )
				
				is_authenticated = check_password( tagged_digest_salt, password )
				"""
		else:
			# directly authenticate without initial search user
			is_authenticated = authenticate_remote( ldap_client, username, password )
			
		if debug:
			if is_authenticated:
				print( "User: %s authenticated OK" % username )
			else:
				print( "User: %s NOT authenticated" % username )
				
	except ldap.LDAPError, ex:
		print( "\nLDAP Error")
		show_dict( ex.message )
		"""
		if type( ex.message ) == dict:
			for( k, v ) in ex.message.iteritems():
				print( "%s: %s" % (k, v) )
		else:
			print( "Error: %s" % ex.message );
		"""
	finally:
		try:
			ldap_client.unbind()
		except ldap.LDAPError, ex:
			print( ex )
			pass

	return is_authenticated



if __name__ == '__main__':
	if debug:
		print( "LDAP PORT: %d" % ldap.PORT )
		print( "LDAP SASL_AVAIL: %d" % ldap.SASL_AVAIL )
		print( "LDAP TLS_AVAIL: %d" % ldap.TLS_AVAIL )
		print( "" )
	
	"""
	#username = "..."
	#password = "..."
	
	is_authenticated = ldap_authenticate( username, password )
	
	if is_authenticated:
		print( "User: '%s' authenticated OK" % username )
	else:
		print( "User: '%s' NOT authenticated" % username )
	"""
	
# [eof]
