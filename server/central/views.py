# -*- coding: utf-8 -*-

"""
Author:		Fons Laan, KNAW IISH - International Institute of Social History
Project:	HSN Mail
Name:		central/views.py
Version:	1.0.0
Goal:		View functions for central

Functions:
def get_huwknd( idnr ):
def get_ovlknd( idnr ):
def get_pkknd(  idnr ):

09-Mar-2016	Created
09-Mar-2016	Changed
"""

# python-future for Python 2/3 compatibility
from __future__ import ( absolute_import, division, print_function, unicode_literals )
from builtins import ( ascii, bytes, chr, dict, filter, hex, input, int, map, next, 
	oct, open, pow, range, round, str, super, zip )

import os
from sys import stderr, exc_info

from .models import ( Huwknd, Ovlknd, Pkknd )


def get_huwknd( idnr ):
	try:
		huwknd_qs = Huwknd.objects.using( "central" ).filter( idnr = idnr ).order_by( "id" )
		return huwknd_qs
	except:
		print( "central/views/get_huwknd( %s )" % idnr )
		type, value, tb = exc_info()
		msg = "Huwknd.objects failed: %s" % value
		print( "%s\n" % msg )



def get_ovlknd( idnr ):
	try:
		ovlknd_qs = Ovlknd.objects.using( "central" ).filter( idnr = idnr ).order_by( "id" ).first()
		return ovlknd_qs
	except:
		print( "central/views/get_ovlknd( %s )" % idnr )
		type, value, tb = exc_info()
		msg = "Ovlknd.objects.filter failed: %s" % value
		print( "%s\n" % msg )



def get_pkknd( idnr ):
	try:
		pkknd_qs = Pkknd.objects.using( "central" ).filter( idnr = idnr ).order_by( "id" ).first()
		return pkknd_qs
	except:
		print( "central/views/get_pkknd( %s )" % idnr )
		type, value, tb = exc_info()
		msg = "Pkknd.objects failed: %s" % value
		print( "%s\n" % msg )

# [eof]
