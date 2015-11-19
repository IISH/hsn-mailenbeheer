# -*- coding: utf-8 -*-

"""
Author:		Fons Laan, KNAW IISH - International Institute of Social History
Project:	HSN Mail
Name:		views.py
Version:	0.1
Goal:		View for op_select

Functions:
def get_locations():
def get_municipalities():
def get_sources():
def get_text_strings():
def get_mails( op_number ):
def get_mails_print():
def put_mailbev( mailbev_req ):
def put_mailhuw( mailhuw_req ):
def put_mailbevreceived( mailbevreceived_req ):
def put_opmutation( opmutation_req ):

26-May-2015	Created
26-Oct-2015	Changed
"""

# python-future for Python 2/3 compatibility
from __future__ import ( absolute_import, division, print_function, unicode_literals )
from builtins import ( ascii, bytes, chr, dict, filter, hex, input, int, map, next, 
	oct, open, pow, range, round, str, super, zip )

import os
from sys import stderr, exc_info

from django.conf import settings

#from mail.models import Gemeente, HsnIdmut, Huwknd, Locarchf, Mail, Plaats
from mail.models import ( ArchiefGemeente, HsnIdmut, Huwknd, Mail, Plaats, 
	TekstFaseA, TekstFaseB, TekstFaseCD, TekstGevonden, TekstReden, TekstVoortgang )


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
		locations = Plaats.objects.all().order_by( "gemnaam" )

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
		msg = "get_locations() failed: %s" % value
		print( "%s\n" % msg )

	return choices_location



def get_municipalities():
	"""
	List of (nr + town) for combobox
	Notice: municipalities from table 'Gemeente', not from table 'Plaats'.
	"""
#	print( "get_municipalities()" )

	choices_municipality = []

	try:
		municipalities = Gemeente.objects.all().order_by( "gemeentenaam" )

		m = 0
		for municipality in municipalities:
			name = municipality.gemeentenaam
			nr   = municipality.gemeentenr
		#	print( nr, name )
			if name is None:
				continue
			
			map = { "idx" : m, "nr" : nr, "name" : name }
			choices_municipality.append( map )
			m += 1
			
	except:
		type, value, tb = exc_info()
		msg = "get_municipalities() failed: %s" % value
		print( "%s\n" % msg )

	return choices_municipality 



def get_sources():
	"""
	List of (town + nr) for GUI combobox
	"""

	choices_source = []

	try:
		sources = ArchiefGemeente.objects.all().order_by( "gemnaam" )

		s = 0
		for source in sources:
			name = source.gemnaam
			nr   = source.gemnr
		#	print( nr, name )
			if name is None:
				continue
			
			map = { "idx" : s, "nr" : nr, "name" : name }
			choices_source.append( map )
			s += 1
			
	except:
		type, value, tb = exc_info()
		msg = "get_sources() failed: %s" % value
		print( "%s\n" % msg )

	return choices_source



def get_text_strings():
	"""
	Lists of fixed strings for comboboxs
	"""
#	print( "get_text_strings()" )
	# Notice: the idx values below are not necessarily identical 
	# to the pk's in the corresponding tables. 

	all_strings = {}
	
	strings = []
	try:
		objects = TekstFaseA.objects.all().order_by( "fase_a" )
		
		o = 0
		for object in objects:
			text = object.fase_a_text
			id   = object.fase_a
		#	print( id, text )
			
			map = { "idx" : o, "id" : id, "text" : text }
			strings.append( map )
			o += 1
			
	except:
		type, value, tb = exc_info()
		msg = "get_text_strings() failed for TekstFaseA: %s" % value
		print( "%s\n" % msg )

	all_strings[ "TekstFaseA" ] = strings
	
	
	strings = []
	try:
		objects = TekstFaseB.objects.all().order_by( "fase_b" )
		
		o = 0
		for object in objects:
			text = object.fase_b_text
			id   = object.fase_b
		#	print( id, text )
			
			map = { "idx" : o, "id" : id, "text" : text }
			strings.append( map )
			o += 1
			
	except:
		type, value, tb = exc_info()
		msg = "get_text_strings() failed for TekstFaseB: %s" % value
		print( "%s\n" % msg )

	all_strings[ "TekstFaseB" ] = strings
	
	
	strings = []
	try:
		objects = TekstFaseCD.objects.all().order_by( "fase_c_d" )
		
		o = 0
		for object in objects:
			text = object.fase_c_d_text
			id   = object.fase_c_d
		#	print( id, text )
			
			map = { "idx" : o, "id" : id, "text" : text }
			strings.append( map )
			o += 1
			
	except:
		type, value, tb = exc_info()
		msg = "get_text_strings() failed for TekstFaseCD: %s" % value
		print( "%s\n" % msg )

	all_strings[ "TekstFaseCD" ] = strings
	
	
	strings = []
	try:
		objects = TekstGevonden.objects.all().order_by( "id" )
		
		o = 0
		for object in objects:
			text = object.text_gevonden
			id   = object.gevonden
		#	print( id, text )
			
			map = { "idx" : o, "id" : id, "text" : text }
			strings.append( map )
			o += 1
			
	except:
		type, value, tb = exc_info()
		msg = "get_text_strings() failed for TekstGevonden: %s" % value
		print( "%s\n" % msg )

	all_strings[ "TekstGevonden" ] = strings
	
	
	strings = []
	try:
		objects = TekstReden.objects.all().order_by( "reden" )
		
		o = 0
		for object in objects:
			text = object.reden_text
			id   = object.reden
		#	print( id, text )
			
			map = { "idx" : o, "id" : id, "text" : text }
			strings.append( map )
			o += 1
			
	except:
		type, value, tb = exc_info()
		msg = "get_text_strings() failed for TekstReden: %s" % value
		print( "%s\n" % msg )

	all_strings[ "TekstReden" ] = strings
	
	
	strings = []
	try:
		objects = TekstVoortgang.objects.all().order_by( "id" )
		
		o = 0
		for object in objects:
			text = object.invoerstatustekst
			id   = object.invoerstatus
		#	print( id, text )
			
			map = { "idx" : o, "id" : id, "text" : text }
			strings.append( map )
			o += 1
			
	except:
		type, value, tb = exc_info()
		msg = "get_text_strings() failed for TekstVoortgang: %s" % value
		print( "%s\n" % msg )

	all_strings[ "TekstVoortgang" ] = strings
	
	return all_strings



def get_mails( op_number ):
	"""
	List of existing mails of OP
	"""
	print( "get_mails()" )

	nmails = 0

	mails_bev = []
	mails_huw = []
	mails_oth = []
	
	try:
		mail_qs = Mail.objects.filter( idnr = op_number ).order_by( "id" )
		
		if mail_qs is None:
			print( "Mail does not contain entries for OP %d", op_number )
		else:
			from qx.views import none2empty
			nmails = mail_qs.count()
			print( "Mail has %d entries for OP %s" % ( nmails, op_number ) )
			for mail in mail_qs:
				mail_dict = {
					"id"          : mail.id,					# AI PK
					"idnr"        : none2empty( mail.idnr ),
					"briefnr"     : none2empty( mail.briefnr ),
					"aard"        : none2empty( mail.aard ),
					"datum"       : none2empty( mail.datum ),
					"periode"     : none2empty( mail.periode ),
					"gemnr"       : none2empty( mail.gemnr ),
					"naamgem"     : none2empty( mail.naamgem ),
					"status"      : none2empty( mail.status ),
					"printdatum"  : none2empty( mail.printdatum ),
					"printen"     : none2empty( mail.printen ),
					"ontvdat"     : none2empty( mail.ontvdat ),
					"opmerk"      : none2empty( mail.opmerk ),
					"opident"     : none2empty( mail.opident ),
					"oppartner"   : none2empty( mail.oppartner ),
					"opvader"     : none2empty( mail.opvader ),
					"opmoeder"    : none2empty( mail.opmoeder ),
					"type"        : none2empty( mail.type ),
					"infoouders"  : none2empty( mail.infoouders ),
					"infopartner" : none2empty( mail.infopartner ),
					"inforeis"    : none2empty( mail.inforeis )
				}
				
				if mail.type == "BEV":
					mails_bev.append( mail_dict )
					if mail.status == '0':
						nstatus0_bev += 1
				elif mail.type == "HUW":
					mails_huw.append( mail_dict )
				else:
					mails_oth.append( mail_dict )
		
	except:
		print( "get_mails()" )
		type, value, tb = exc_info()
		msg = "Mail.objects.filter failed: %s" % value
		print( "%s\n" % msg )

	mails = {
		"bev" : mails_bev,
		"huw" : mails_huw,
		"oth" : mails_oth
	}
	
	return mails



def get_mails_print():
	"""
	List of mails with status 0 for printing "BEV" mails (ignoring "HUW" mails)
	"""
	print( "get_mails_print()" )

#	nmails_bev = 0
#	nmails_huw = 0
	
	print_bev = []
	print_huw = []

	try:
		mail_qs = Mail.objects.filter( status = 0, type = "BEV" ).order_by( "id" )
		
		if mail_qs is None:
			print( "Mail does not contain entries with status = 0" )
		else:
			nmails_bev = mail_qs.count()
			for mail in mail_qs:
				mail_dict = { "id" : mail.id, "idnr" : mail.idnr }
				print_bev.append( mail_dict )

	except:
		print( "get_mails_print()" )
		type, value, tb = exc_info()
		msg = "Mail.objects.filter failed: %s" % value
		print( "%s\n" % msg )


#	bev = { "nmails" : nmails_bev }
#	huw = { "nmails" : nmails_huw }
	
	mails =  { "bev" : print_bev, "huw" : print_huw }
	
	return mails



def put_mailbev( mailbev_req ):
	"""
	We have the pk (id) in the client data. 
	Update the Mail table in 3 steps: 
	1) if the pk is empty, we do a create
	2) if the pk is non-empty, we do an update
	3) delete the records from the list pkdeleted
	"""
	
	status = "OK"
	msg = "Nothing done"
	
	idnr  = mailbev_req.get( "idnr" )
	nrows = mailbev_req.get( "nrows" )
	rdata = mailbev_req.get( "rdata" )
	print( "idnr:", idnr, "nrows:", nrows )
	
	nupdated = 0
	ncreated = 0
	ndeleted = 0
	
	# step 1: update and/or create records
	for row in rdata:
	#	print( row )
		
		id           = row.get( "id" )
		idnr         = row.get( "idnr" )
		aard         = row.get( "kind" )
		datum        = row.get( "date" )
		periode      = row.get( "period" )
		gemnr        = row.get( "location_nr" )
		naamgem      = row.get( "location" )
		status       = row.get( "status" )
		opmerk       = row.get( "remarks" )
		opident      = row.get( "op_ident" )
		oppartner    = row.get( "op_partner" )
		opvader      = row.get( "op_father" )
		opmoeder     = row.get( "op_mother" )
		mtype        = row.get( "type" )
		infoouders   = row.get( "info_parents" )
		infopartner  = row.get( "info_partner" )
		inforeis     = row.get( "info_journey" )
		
		try:
			id = int( id )
		except:
			id = None
		
		try:
			idnr = int( idnr )
		except:
			idnr = None
		
		try:
			gemnr = int( gemnr )
		except:
			gemnr = None
		
		mailbev_dict = {
			"id"          : id,
			"idnr"        : idnr,
			"aard"        : aard,
			"datum"       : datum,
			"periode"     : periode,
			"gemnr"       : gemnr,
			"naamgem"     : naamgem,
			"status"      : status,
			"opmerk"      : opmerk,
			"opident"     : opident,
			"oppartner"   : oppartner,
			"opvader"     : opvader,
			"opmoeder"    : opmoeder,
			"type"        : mtype,
			"infoouders"  : infoouders,
			"infopartner" : infopartner,
			"inforeis"    : inforeis
		}
		
		if id is None:
			# new row (no pk)
			try:
				status = "OK"
				ncreated += 1
				mail = Mail.objects.create( **mailbev_dict )
				print( "created id: %s for idnr: %s" % ( mail.id, idnr ) )
			except:
				status = "ERROR"
				print( "mail/views/put_mailbev() idnr = %s" % idnr )
				type, value, tb = exc_info()
				msg = "Mail.objects.create() failed: %s" % value
				print( "%s\n" % msg )
				print( mailbev_dict )
		
		else:
			# update row
			try:
				status = "OK"
				nupdated += 1
				mail = Mail.objects.get( id = id )
				mail = Mail.objects.filter( id = id ).update( **mailbev_dict )
				print( "updated id: %s for idnr: %s" % ( id, idnr ) )

			except:
				status = "ERROR"
				print( "mail/views/put_mailbev() idnr = %s" % idnr )
				type, value, tb = exc_info()
				msg = "Mail.objects.update() failed: %s" % value
				print( "%s\n" % msg )
				print( mailbev_dict )
	
	pk_deleted = mailbev_req.get( "pkdeleted" )
	for id in pk_deleted:
		try:
			status = "OK"
			ndeleted += 1
			mail = Mail.objects.get( id = id )
			Mail.objects.filter( id = id ).delete()
			print( "deleted id: %s for idnr: %s" % ( id, mail.idnr ) )
		except:
			status = "ERROR"
			print( "mail/views/put_mailbev() idnr = %s" % idnr )
			type, value, tb = exc_info()
			msg = "Mail.objects.delete() failed: %s" % value
			print( "%s\n" % msg )
			print( mailbev_dict )


	msg = "put_mailhuw() idnr = %s, updated: %d, created: %d, deleted: %d" % \
		( idnr, nupdated, ncreated, ndeleted )
	print( msg )
	
	return status, msg



def put_mailhuw( mailhuw_req ):
	"""
	We have the pk (id) in the client data. 
	Update the Mail table in 3 steps: 
	1) if the pk is empty, we do a create
	2) if the pk is non-empty, we do an update
	3) delete the records from the list pkdeleted
	"""
	
	status = "OK"
	msg = "Nothing done"
	
	idnr  = mailhuw_req.get( "idnr" )
	nrows = mailhuw_req.get( "nrows" )
	rdata = mailhuw_req.get( "rdata" )
	print( "idnr:", idnr, "nrows:", nrows )
	
	nupdated = 0
	ncreated = 0
	ndeleted = 0
	
	# step 1: update and/or create records
	for row in rdata:
	#	print( row )
		id        = row.get( "id" )
		idnr      = row.get( "idnr" )
		aard      = row.get( "kind" )
		datum     = row.get( "date" )
		periode   = row.get( "period" )
		gemnr     = row.get( "location_nr" )
		naamgem   = row.get( "location" )
		status    = row.get( "status" )
		opmerk    = row.get( "remarks" )
		opident   = row.get( "op_ident" )
		oppartner = row.get( "op_partner" )
		opvader   = row.get( "op_father" )
		opmoeder  = row.get( "op_mother" )
		type      = row.get( "type" )
		
		try:
			id = int( id )
		except:
			id = None
		
		try:
			idnr = int( idnr )
		except:
			idnr = None
		
		try:
			gemnr = int( gemnr )
		except:
			gemnr = None
		
		mailhuw_dict = {
			"id"        : id,
			"idnr"      : idnr,
			"aard"      : aard,
			"datum"     : datum,
			"periode"   : periode,
			"gemnr"     : gemnr,
			"naamgem"   : naamgem,
			"status"    : status,
			#"opmerk"    : opmerk,
			"opident"   : opident,
			"oppartner" : oppartner,
			#"opvader"   : opvader,
			#"opmoeder"  : opmoeder,
			"type"      : type
		}
		
		if id is None:
			# new row (no pk)
			try:
				status = "OK"
				ncreated += 1
				mail = Mail.objects.create( **mailhuw_dict )
				print( "created id: %s for idnr: %s" % ( mail.id, idnr ) )
			except:
				status = "ERROR"
				print( "mail/views/put_mailhuw() idnr = %s" % idnr )
				type, value, tb = exc_info()
				msg = "Mail.objects.create() failed: %s" % value
				print( "%s\n" % msg )
				print( mailhuw_dict )
		
		else:
			# update row
			try:
				status = "OK"
				nupdated += 1
				mail = Mail.objects.get( id = id )
				mail = Mail.objects.filter( id = id ).update( **mailhuw_dict )
				print( "updated id: %s for idnr: %s" % ( mail.id, idnr ) )

			except:
				status = "ERROR"
				print( "mail/views/put_mailhuw() idnr = %s" % idnr )
				type, value, tb = exc_info()
				msg = "Mail.objects.update() failed: %s" % value
				print( "%s\n" % msg )
				print( mailbev_dict )
	
	pk_deleted = mailhuw_req.get( "pkdeleted" )
	for id in pk_deleted:
		try:
			status = "OK"
			ndeleted += 1
			mail = Mail.objects.get( id = id )
			Mail.objects.filter( id = id ).delete()
			print( "deleted id: %s for idnr: %s" % ( mail.id, idnr ) )
		except:
			status = "ERROR"
			print( "mail/views/put_mailhuw() idnr = %s" % idnr )
			type, value, tb = exc_info()
			msg = "Mail.objects.delete() failed: %s" % value
			print( "%s\n" % msg )
			print( mailhuw_dict )


	msg = "put_mailhuw() idnr = %s, updated: %d, created: %d, deleted: %d" % \
		( idnr, nupdated, ncreated, ndeleted )
	print( msg )
	
	return status, msg



def put_mailbevreceived( mailbevreceived_req ):
	"""
	Update the mail status and set the mail received date
	"""
	print( "put_mailbevreceived()" )
	
	ids   = mailbevreceived_req.get( "ids" )
	idnr  = mailbevreceived_req.get( "idnr" )
	fdate = mailbevreceived_req.get( "fdate" )
	
	print( "ids:", ids, "idnr:", idnr, "fdate:", fdate )
	
	status = "OK"
	msg = ""
	
	mailbev_dict = { "status" : 9, "ontvdat" : fdate }

	for id in ids:
		print( "updating id: %s of idnr: %s" % ( id, idnr ) )
		try:
			status = "OK"
			mail = Mail.objects.filter( id = id ).update( **mailbev_dict )
			print( "updated id: %s for idnr: %s" % ( mail.id, idnr ) )
		except:
			status = "ERROR"
			print( "mail/views/put_mailbevreceived() id = %s, idnr = %s" % ( id, idnr ) )
			type, value, tb = exc_info()
			msg = "Mail.objects.update() failed: %s" % value
			print( "%s\n" % msg )
			print( mailbev_dict )

			return status, msg

	return status, msg



def put_opmutation( opmutation_req ):
	"""
	Update the mutation table with a new mutation for the OP
	"""
	print( "put_opmutation()" )
	
	idnr = opmutation_req.get( "idnr" )
	
	status = "OK"
	msg = ""
	
	opmutation_dict = {
		"idnr"         : idnr,
		"id_origin"    : opmutation_req.get( "id_origin" ),
		"source"       : opmutation_req.get( "source" ),
		
		"rp_family"    : opmutation_req.get( "lastname" ),
		"rp_prefix"    : opmutation_req.get( "prefix" ),
		"rp_firstname" : opmutation_req.get( "firstname" ),
		
		"rp_b_day"     : opmutation_req.get( "birth_day" ),
		"rp_b_month"   : opmutation_req.get( "birth_month" ),
		"rp_b_year"    : opmutation_req.get( "birth_year" ),
		
		"rp_b_place"   : opmutation_req.get( "birthplace" ),
		"rp_b_sex"     : opmutation_req.get( "gender" ),
		
		"remarks"      : opmutation_req.get( "remarks" )
	}
	
	valid_day = opmutation_req.get( "valid_day" )
	if valid_day is not None and valid_day != "":
		opmutation_dict[ "valid_day"  ] = valid_day
	
	valid_month = opmutation_req.get( "valid_month" )
	if valid_month is not None and valid_month != "":
		opmutation_dict[ "valid_month"  ] = valid_month
	
	valid_year = opmutation_req.get( "valid_year" )
	if valid_year is not None and valid_year != "":
		opmutation_dict[ "valid_year"  ] = valid_year
	
	print( "adding mutation for idnr: %s" % idnr )
	print( opmutation_dict )
	
	try:
		status = "OK"
		opmutation = HsnIdmut.objects.create( **opmutation_dict )
		print( "created mutation for idnr: %s" % idnr )
		print( opmutation )

	except:
		status = "ERROR"
		print( "mail/views/put_opmutation() idnr = %s" % idnr )
		type, value, tb = exc_info()
		msg = "HsnIdmut.objects.update() failed: %s" % value
		print( "%s\n" % msg )
		print( opmutation_dict )

		return status, msg

	return status, msg

# [eof]
