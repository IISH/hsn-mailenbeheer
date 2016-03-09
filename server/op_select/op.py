# -*- coding: utf-8 -*-

"""
Author:		Fons Laan, KNAW IISH - International Institute of Social History
Project:	HSN Mail
Name:		op.py
Version:	1.0.0
Goal:		'OP' te Onderzoeken Persoon (person to be investigated) functions

Functions:
def get_op_info( op_number ):
def get_id_change_manual( op_number ):
#def get_id_change_auto( op_number ):

09-Jun-2015	Created
08-Mar-2016	Split-off hsn_central & hsn_reference db's
09-Mar-2016	Changed
"""

# python-future for Python 2/3 compatibility
from __future__ import ( absolute_import, division, print_function, unicode_literals )
from builtins import ( ascii, bytes, chr, dict, filter, hex, input, int, map, next, 
	oct, open, pow, range, round, str, super, zip )

from sys import stderr, exc_info

from mail.models import HsnIdmut
from reference.views import get_hsnrp


def get_op_info( op_number ):
	"""
	get birth info from table Hsnrp
	id_origin values: >=10 and < 17
	a given idnr may occur multiple times
	*_firstname is actually firstnames
	"""
	
	op_info_list = []
	if op_number == "":
		print( "op/get_op_info(): empty op_number: doing nothing" )
		return op_info_list
	
	print( "op/get_op_info():", op_number )
	
	hsnrp_qs = get_hsnrp( op_number )
	
	if hsnrp_qs is None:
		print( "Hsnrp entry idnr %d does not exist", op_number )
	else:
		from qx.views import none2empty
		for hsnrp in hsnrp_qs:
			id           = hsnrp.id				# AI PK
			idnr         = none2empty( hsnrp.idnr )
			id_origin    = none2empty( hsnrp.id_origin )
			project      = none2empty( hsnrp.project )
			gemnr        = none2empty( hsnrp.gemnr )
			valid_day    = none2empty( hsnrp.valid_day )
			valid_month  = none2empty( hsnrp.valid_month )
			valid_year   = none2empty( hsnrp.valid_year )
			rp_family    = none2empty( hsnrp.rp_family )
			rp_prefix    = none2empty( hsnrp.rp_prefix )
			rp_firstname = none2empty( hsnrp.rp_firstname )
			rp_b_day     = none2empty( hsnrp.rp_b_day )
			rp_b_month   = none2empty( hsnrp.rp_b_month )
			rp_b_year    = none2empty( hsnrp.rp_b_year )
			rp_b_sex     = none2empty( hsnrp.rp_b_sex )
			rp_b_place   = none2empty( hsnrp.rp_b_place )
			rp_b_prov    = none2empty( hsnrp.rp_b_prov )
			rp_b_coh     = none2empty( hsnrp.rp_b_coh )
			mo_family    = none2empty( hsnrp.mo_family )
			mo_prefix    = none2empty( hsnrp.mo_prefix )
			mo_firstname = none2empty( hsnrp.mo_firstname )
			fa_family    = none2empty( hsnrp.fa_family )
			fa_prefix    = none2empty( hsnrp.fa_prefix )
			fa_firstname = none2empty( hsnrp.fa_firstname )
			
			op_info_dict = {}
			op_info_dict[ "id" ]           = id
			op_info_dict[ "idnr" ]         = idnr
			op_info_dict[ "id_origin" ]    = id_origin
			op_info_dict[ "project" ]      = project
			op_info_dict[ "gemnr" ]        = gemnr
			op_info_dict[ "valid_day" ]    = valid_day
			op_info_dict[ "valid_month" ]  = valid_month
			op_info_dict[ "valid_year" ]   = valid_year
			op_info_dict[ "rp_family" ]    = rp_family
			op_info_dict[ "rp_prefix" ]    = rp_prefix
			op_info_dict[ "rp_firstname" ] = rp_firstname
			op_info_dict[ "rp_b_day" ]     = rp_b_day
			op_info_dict[ "rp_b_month" ]   = rp_b_month
			op_info_dict[ "rp_b_year" ]    = rp_b_year
			op_info_dict[ "rp_b_sex" ]     = rp_b_sex
			op_info_dict[ "rp_b_place" ]   = rp_b_place
			op_info_dict[ "rp_b_prov" ]    = rp_b_prov
			op_info_dict[ "rp_b_coh" ]     = rp_b_coh
			op_info_dict[ "mo_family" ]    = mo_family
			op_info_dict[ "mo_prefix" ]    = mo_prefix
			op_info_dict[ "mo_firstname" ] = mo_firstname 
			op_info_dict[ "fa_family" ]    = fa_family
			op_info_dict[ "fa_prefix" ]    = fa_prefix
			op_info_dict[ "fa_firstname" ] = fa_firstname
			
			# some fields not in the table
			op_info_dict[ "remarks" ] = ""
		
			valid_date = "%s/%s/%s" % ( valid_day, valid_month, valid_year )
			op_info_dict[ "valid_date" ] = valid_date
			
			rp_b_date = "%s/%s/%s" % ( rp_b_day, rp_b_month, rp_b_year )
			op_info_dict[ "rp_b_date" ] = rp_b_date
			
			display_rp_family = rp_family
			if rp_prefix != "":
				display_rp_family +=  ", " + rp_prefix
			
			if int( id_origin ) == 10:
				display_str = "%s %s, %s [%s], geboren %s/%s/%s te %s" % ( 
					idnr, display_rp_family, rp_firstname, rp_b_sex, rp_b_day, rp_b_month, rp_b_year, rp_b_place )
			else:
				display_str = "%s, %s [%s], geboren %s/%s/%s te %s" % ( 
					display_rp_family, rp_firstname, rp_b_sex, rp_b_day, rp_b_month, rp_b_year, rp_b_place )
			
			op_info_dict[ "display_str" ] = display_str
			
			op_info_list.append( op_info_dict )


	op_info_list_manual = get_id_change_manual( op_number )
	for op_info in op_info_list_manual:
		op_info_list.append( op_info )

	return op_info_list



def get_id_change_manual( op_number ):
	"""
	get id change id info from table HsnIdmut
	id_origin values: 17 and 18
	a given idnr may occur multiple times
	*_firstname is actually firstnames
	"""
	print( "op/get_id_change_manual():", op_number )

	# Get Identification mutations info from table HsnIdmut
	# Such id mutations has been created manually via the hsnmailenbeheer GUI
	# There can also be automatic id changes from table Hsnrp
	
	op_info_list = []
		
	try:
		hsnidmut_qs = HsnIdmut.objects.filter( idnr = op_number )

		if hsnidmut_qs is None:
			print( "HsnIdmut entry %d does not exist", op_number )
		else:
			from qx.views import none2empty
			for hsnidmut in hsnidmut_qs:
				id           = hsnidmut.id				# AI PK
				idnr         = none2empty( hsnidmut.idnr )
				id_origin    = none2empty( hsnidmut.id_origin )
				rp_family    = none2empty( hsnidmut.rp_family )
				rp_prefix    = none2empty( hsnidmut.rp_prefix )
				rp_firstname = none2empty( hsnidmut.rp_firstname )
				rp_b_day     = none2empty( hsnidmut.rp_b_day )
				rp_b_month   = none2empty( hsnidmut.rp_b_month )
				rp_b_year    = none2empty( hsnidmut.rp_b_year )
				rp_b_place   = none2empty( hsnidmut.rp_b_place )
				rp_b_sex     = none2empty( hsnidmut.rp_b_sex )
				valid_day    = none2empty( hsnidmut.valid_day )
				valid_month  = none2empty( hsnidmut.valid_month )
				valid_year   = none2empty( hsnidmut.valid_year )
				remarks      = none2empty( hsnidmut.remarks )
				
				op_info_dict = {}
				op_info_dict[ "id" ]           = id
				op_info_dict[ "idnr" ]         = idnr
				op_info_dict[ "id_origin" ]    = id_origin
				op_info_dict[ "rp_family" ]    = rp_family
				op_info_dict[ "rp_prefix" ]    = rp_prefix
				op_info_dict[ "rp_firstname" ] = rp_firstname
				op_info_dict[ "rp_b_day" ]     = rp_b_day
				op_info_dict[ "rp_b_year" ]    = rp_b_year
				op_info_dict[ "rp_b_place" ]   = rp_b_place
				op_info_dict[ "rp_b_sex" ]     = rp_b_sex
				op_info_dict[ "valid_day" ]    = valid_day
				op_info_dict[ "valid_month" ]  = valid_month
				op_info_dict[ "valid_year" ]   = valid_year
				op_info_dict[ "remarks" ]      = remarks

				# some fields not in the table
				valid_date = "%s/%s/%s" % ( valid_day, valid_month, valid_year )
				op_info_dict[ "valid_date" ]   = valid_date

				rp_b_date = "%s/%s/%s" % ( rp_b_day, rp_b_month, rp_b_year )
				op_info_dict[ "rp_b_date" ] = rp_b_date
				
				display_rp_family = rp_family
				if rp_prefix != "":
					display_rp_family +=  ", " + rp_prefix
				
				display_str = "%s, %s [%s], geboren %s/%s/%s te %s" % ( 
					display_rp_family, rp_firstname, rp_b_sex, rp_b_day, rp_b_month, rp_b_year, rp_b_place )
				
				op_info_dict[ "display_str" ] = display_str
				
				op_info_list.append( op_info_dict )
	except:
		print( "op/get_id_change_manual()" )
		type, value, tb = exc_info()
		msg = "HsnIdmut.objects.get failed: %s" % value
		print( "%s\n" % msg )

	return op_info_list



"""
def get_id_change_auto( op_number ):
#	print( "op/get_id_change_auto:", op_number )
	
	auto_date   = ""
	auto_fields = {}
	auto_string = ""
	auto_remark = ""

	# Get Identification mutations info from table Hsnrp
	# Such id mutations have been created automatically
	# There can also be manual id changes from table HsnIdmut

	info = get_hsnrp( op_number )

	if info is None:
		print( "Hsnrp entry %d does not exist", op_number )
	else:
		idnr         = info.idnr
		rp_family    = info.rp_family
		rp_prefix    = info.rp_prefix
		rp_firstname = info.rp_firstname
		rp_b_day     = info.rp_b_day
		rp_b_month   = info.rp_b_month
		rp_b_year    = info.rp_b_year
		rp_b_place   = info.rp_b_place
		rp_b_sex     = info.rp_b_sex
		valid_day    = info.valid_day
		valid_month  = info.valid_month
		valid_year   = info.valid_year
		
		if rp_prefix is None: rp_prefix = ""
		
		print( "idnr:",     idnr )
		print( "anaam:",    rp_family )
		print( "prefix:",   rp_prefix )
		print( "vnaam:",    rp_firstname )
		print( "gebdag:",   rp_b_day )
		print( "gebmnd:",   rp_b_month )
		print( "gebjr:",    rp_b_year )
		print( "gebpl:",    rp_b_place )
		print( "gebsex:",   rp_b_sex )
		print( "startdag:", valid_day )
		print( "startmnd:", valid_month )
		print( "startjar:", valid_year )

		auto_fields[ "idnr" ]     = idnr
		auto_fields[ "anaam" ]    = rp_family
		auto_fields[ "prefix" ]   = rp_prefix
		auto_fields[ "vnaam" ]    = rp_firstname
		auto_fields[ "gebdag" ]   = rp_b_day
		auto_fields[ "gebmnd" ]   = rp_b_month
		auto_fields[ "gebjr" ]    = rp_b_year
		auto_fields[ "gebpl" ]    = rp_b_place
		auto_fields[ "gebsex" ]   = rp_b_sex
		auto_fields[ "startdag" ] = valid_day
		auto_fields[ "startmnd" ] = valid_month
		auto_fields[ "startjar" ] = valid_year

		auto_date = "%s/%s/%s" % ( valid_day, valid_month, valid_year )
		
		display_rp_family = rp_family
		if rp_prefix != "":
			display_rp_family +=  " " + rp_prefix
		
		auto_string = "%s %s, %s [%s] * %s/%s/%s %s" % ( 
			idnr, display_rp_family, rp_firstname, rp_b_sex, valid_day, valid_month, valid_year, rp_b_place )
		
		auto_remark = ""	# not present in Hsnrp
	
	id_auto = {
		"date"   : auto_date,
		"fields" : auto_fields,
		"string" : auto_string,
		"remark" : auto_remark
	}

	return id_auto
"""

# [eof]
