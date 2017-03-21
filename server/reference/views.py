# -*- coding: utf-8 -*-

"""
Author:		Fons Laan, KNAW IISH - International Institute of Social History
Project:	HSN Mail
Name:		reference/views.py
Version:	1.0.1
Goal:		View functions for reference

Functions:
def get_opsex( idnr ):
def get_locations():
def get_location_by_gemnr( gemnr ):
def get_location_by_gemnaam( gemnaam ):

09-Mar-2016	Created
20-Mar-2017	Changed
"""

# future-0.16.0 imports for Python 2/3 compatibility
from __future__ import ( absolute_import, division, print_function, unicode_literals )
from builtins import ( ascii, bytes, chr, dict, filter, hex, input, int, list, map, 
    next, object, oct, open, pow, range, round, super, str, zip )

import os
from sys import stderr, exc_info

from .models import ( Plaats, Hsnrp )


def get_hsnrp( idnr ):
	try:
		hsnrp_qs = Hsnrp.objects.using( "reference" ).filter( idnr = idnr )
		return hsnrp_qs
	except:
		print( "reference/views/get_hsnrp( %s )" % idnr )
		type, value, tb = exc_info()
		msg = "Hsnrp.objects failed: %s" % value
		print( "%s\n" % msg )



def get_opsex( idnr ):
	opsex = None
	# get birth info from Hsnrp
	try:
		birth_info = Hsnrp.objects.using( "reference" ).filter( idnr = idnr ).last()	# idnr is not pk
		if birth_info is not None:
			opsex = birth_info.rp_b_sex
	except:
		print( "reference/views/get_opsex( %s )" % idnr )
		type, value, tb = exc_info()
		msg = "Hsnrp.objects failed: %s" % value
		print( "%s\n" % msg )

	return opsex



def get_locations():
	"""
	List of (nr + location) for combobox. 
	Notice: locations from table 'Plaats'. 
	
	Some gemnaam occur more than once, but identical gemnaam have identical gemnr. 
	So we need only single occurrences in the list for all unique name/nr pairs. 
	"""
#	print( "get_locations()" )

	choices_location = []
	nr_list = []
	
	try:
		locations = Plaats.objects.using( "reference" ).all().order_by( "gemnaam" )

		for location in locations:
			name = location.gemnaam
			nr   = location.gemnr
		#	print( nr, name )
			
			if name is None:
				continue
			
			try:
				nr_list.index( nr )
				# already in list
			except:
				nr_list.append( nr )
				map = { "nr" : nr, "name" : name }
				choices_location.append( map )

	except:
		type, value, tb = exc_info()
		msg = "reference/views/get_locations() failed: %s" % value
		print( "%s\n" % msg )

	return choices_location



def get_location_by_gemnr( gemnr ):
	try:
		plaats_qs = Plaats.objects.using( "reference" ).filter( gemnr = gemnr ).first()
		return plaats_qs
	except:
		print( "reference/views/get_location_by_gemnr()" )
		type, value, tb = exc_info()
		msg = "Plaats.objects failed: %s" % value
		print( "%s\n" % msg )



def get_location_by_gemnaam( gemnaam ):
	try:
		plaats_qs = Plaats.objects.using( "reference" ).get( gemnaam = gemnaam )
		return plaats_qs
	except:
		print( "reference/views/get_location_by_gemnaam()" )
		type, value, tb = exc_info()
		msg = "Plaats.objects failed: %s" % value
		print( "%s\n" % msg )

# [eof]
