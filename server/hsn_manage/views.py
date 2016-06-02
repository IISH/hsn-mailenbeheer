# -*- coding: utf-8 -*-

"""
Author:		Fons Laan, KNAW IISH - International Institute of Social History
Project:	HSN Mail
Name:		hsn_manage/views.py
Version:	1.0.0
Goal:		View for hsn_manage

Functions:
def normalize_date( date_in )
def get_marriages( op_numstr )
def get_marriages_huwknd( op_numstr )
def get_marriages_mail( op_numstr )
def get_deaths( op_numstr )
def get_death_ovlknd( op_numstr )
def get_death_pkknd( op_numstr )
def get_deaths_hsnmanage( op_numstr )
def get_partners( op_number )
def get_partners_huwknd( op_number )
def get_partners_mail( op_number )
def get_missing( op_numstr )
def get_hsnmanage( op_numstr )
def get_voortgang( invoerstatus )
def put_hsnmanage( fields )
def put_hsnmanagemissing( missing_req )

02-Jun-2015	Created
08-Mar-2016	Split-off hsn_central & hsn_reference db's
15-Mar-2016	Changed
"""

# python-future for Python 2/3 compatibility
from __future__ import ( absolute_import, division, print_function, unicode_literals )
from builtins import ( ascii, bytes, chr, dict, filter, hex, input, int, map, next, 
	oct, open, pow, range, round, str, super, zip )

import os.path
from sys import stderr, exc_info
from sys import path
import numbers

from django.core.exceptions import ObjectDoesNotExist

from mail.models import ( HsnBeheer, HsnKwyt, Mail, TekstVoortgang, TekstFaseA, TekstFaseB, TekstFaseCD )
from reference.views import ( get_location_by_gemnr, get_location_by_gemnaam )
from central.views import ( get_huwknd, get_ovlknd, get_pkknd )

from hsnmailenbeheer.settings import PROJECT_ROOT
path.append( os.path.join( PROJECT_ROOT, "op_select" ) )


def normalize_date( date_in ):
	date = ""

	# we try to normalize the dates to dd-mm-yyyy because they 
	# must be compared to the dates from the Huwknd table
	if date_in.count( '/' ) == 2:
		trio = date_in.split( '/' )
		try:
			mday   = int( trio[ 0 ] )
			mmonth = int( trio[ 1 ] )
			myear  = int( trio[ 2 ] )
			date = "%02d/%02d/%04d" % ( mday, mmonth, myear)
		except:
			date = datum_in
	
	elif date_in.count( '-' ) == 2:
		trio = date_in.split( '-' )
		try:
			mday   = int( trio[ 0 ] )
			mmonth = int( trio[ 1 ] )
			myear  = int( trio[ 2 ] )
			date = "%02d/%02d/%04d" % ( mday, mmonth, myear)
		except:
			date = date_in
	else:
		date = date_in
			
	return date



def get_marriages( op_numstr ):
	print( "hsn_manage/views/get_marriages:", op_numstr )

	marriages_huwknd = get_marriages_huwknd( op_numstr )

	marriages = []
	for marriage_huwknd in marriages_huwknd:
		marriage_str = marriage_huwknd[ "date" ] + " " + marriage_huwknd[ "place" ] + " " + marriage_huwknd[ "comment" ]
		
		partner_dict = marriage_huwknd[ "partner" ]
		if partner_dict[ "sex" ] == 'm':
			marriage_str += ", echtgenoot: "
		else:
			marriage_str += ", echtgenote: "
		marriage_str += partner_dict[ "fullname" ]
		marriages.append( marriage_str )

	marriages_mail = get_marriages_mail( op_numstr )
	print( marriages_mail )

	for marriage_mail in marriages_mail:
		date_mail = marriage_mail[ "date" ]
		duplicate = False
		
		for marriage_huwknd in marriages_huwknd:
			date_huwknd = marriage_huwknd[ "date" ]
			if date_mail == date_huwknd:
				duplicate = True
				break
				
		if not duplicate:
			marriage_str = marriage_mail[ "date" ] + " " + marriage_mail[ "place" ] + " " + marriage_mail[ "comment" ]
			if marriage_mail[ "partner" ] != "":
				marriage_str += ", partner: "
				marriage_str += marriage_mail[ "partner" ]
			marriages.append( marriage_str )
	
	return marriages



def get_marriages_huwknd( op_numstr ):
	print( "hsn_manage/views/get_marriages_huwknd:", op_numstr )

	marriages = []

	# get marriage info info from Huwknd
	huwknd_qs = get_huwknd( op_numstr )

	if huwknd_qs is not None:
		for huwknd in huwknd_qs:
			mar_date  = "%02d/%02d/%04d" % ( int(huwknd.hdag), int(huwknd.hmaand), int(huwknd.hjaar) )
			
			# construct partner info
			gebsex = huwknd.gebsex
			if gebsex == 'm':					# OP is man
				partnersex = 'v'
				familyname = huwknd.anmhv		# familyname wife
				firstname1 = huwknd.vrn1hv		# firstname1 wife
				firstname2 = huwknd.vrn2hv		# firstname2 wife
				firstname3 = huwknd.vrn3hv		# firstname3 wife
			elif gebsex == 'v':					# OP is woman
				partnersex = 'm'
				familyname = huwknd.anmhm		# familyname husband
				firstname1 = huwknd.vrn1hm		# firstname1 husband
				firstname2 = huwknd.vrn2hm		# firstname2 husband
				firstname3 = huwknd.vrn3hm		# firstname3 husband
			
			if familyname is None: familyname = ""
			if firstname1 is None: firstname1 = ""
			if firstname2 is None: firstname2 = ""
			if firstname3 is None: firstname3 = ""
			
			fullname = familyname
			fullname += ", "
			fullname += firstname1
			if firstname2 != "":
				fullname += " "
				fullname += firstname2
			if firstname3 != "":
				fullname += " "
				fullname += firstname3
			
			partner = ""
			if gebsex == 'm' or gebsex == 'v':
				partner = {
					"sex"        : partnersex,
					"familyname" : familyname,
					"firstname1" : firstname1,
					"firstname2" : firstname2,
					"firstname3" : firstname3,
					"fullname"   : fullname
				}
				print( "partner:", partner )
			
			mar = { "date" : mar_date, "place" : huwknd.hplts, "comment" : "ingevoerd", "partner" : partner }
			print( "marriage:", mar )
			
			marriages.append( mar )
	else:
		print( "Huwknd entry %s does not exist", op_numstr )

	return marriages



def get_marriages_mail( op_numstr ):
	print( "hsn_manage/views/get_marriages_mail:", op_numstr )

	marriages = []

	# get marriage info info from Mail
	try:
		mail_qs = Mail.objects.using( "mail" ).filter( idnr = op_numstr, type = "HUW" ).order_by( "id" )

		if mail_qs is not None:
			for mail in mail_qs:
				mar_date = normalize_date( mail.datum )
				
				partner = mail.oppartner
				if partner is None: partner = ""
				
				marriage = { "date" : mar_date, "place" : mail.naamgem, "comment" : "in te voeren", "partner" : partner }
				print( "marriage:", marriage )
				marriages.append( marriage )
		else:
			print( "Mail entry %s does not exist", op_numstr )

	except:
		print( "hsn_manage/views/get_marriages_mail( %s )" % op_numstr)
		type, value, tb = exc_info()
		msg = "Mail.objects.filter failed: %s" % value
		print( "%s\n" % msg )

	return marriages



def get_deaths( op_numstr ):
	deaths = []
	
	death_ovlknd = get_death_ovlknd( op_numstr )
	if death_ovlknd is not None:
		deaths.append( death_ovlknd )
	
	death_pkknd = get_death_pkknd( op_numstr )
	if death_pkknd is not None:
		deaths.append( death_pkknd )
	
	death_hsnmanage = get_death_hsnmanage( op_numstr )
	if death_hsnmanage is not None:
		# sometimes the death location is not [yet] present in the HsnBeheer table, 
		# but we [sometimes] can display it from the Ovlknd table
		if death_hsnmanage.get( "death_location" ) == "" and death_ovlknd is not None:
			death_hsnmanage[ "death_location" ] = death_ovlknd.get( "death_location" )
		deaths.append( death_hsnmanage )
	
	return deaths



def get_death_ovlknd( op_numstr ):
	print( "hsn_manage/views/get_death_ovlknd:", op_numstr )

	death = None
	death_location = ""
	death_location_nr = ""

	# get death info info from Ovlknd
	entry = get_ovlknd( op_numstr )
	
	if entry is None:
		print( "Ovlknd entry %s does not exist" % op_numstr )
	else:
		from qx.views import none2empty
		death_location    = none2empty( entry.oacgemnm )
		death_location_nr = none2empty( entry.oacgemnr )
		
		death = { 
			"table_name"        : "Ovlknd", 
			"edit"              : False, 
			"death_day"         : entry.ovldag, 
			"death_month"       : entry.ovlmnd, 
			"death_year"        : entry.ovljr, 
			"death_location"    : death_location,
			"death_location_nr" : death_location_nr
		}
		print( death )
	
	
	# sometimes the death location is empty, but it might be retrieved via the nr
	if death is not None and death_location == "" and death_location_nr != "":
		plaats_qs = get_location_by_gemnr( death_location_nr )
		
		if plaats_qs is not None:
			death_location = plaats_qs.gemnaam
			death[ "death_location" ] = death_location
		else:
			print( "Plaats with gemnr %s does not exist", death_location_nr )
	
	return death



def get_death_pkknd( op_numstr ):
	print( "hsn_manage/views/get_death_pkknd:", op_numstr )

	death = None

	# get death info info from Pkknd
	entry = get_pkknd( op_numstr )

	if entry is not None:
		death = { 
			"table_name"     : "Pkknd", 
			"edit"           : False, 
			"death_day"      : entry.odgperp, 
			"death_month"    : entry.omdperp, 
			"death_year"     : entry.ojrperp, 
			"death_location" : entry.oplperp
		}
		print( death )
	else:
		print( "Pkknd entry %s does not exist" % op_numstr )

	return death



def get_death_hsnmanage( op_numstr ):
	print( "hsn_manage/views/get_death_hsnmanage:", op_numstr )

	death = None

	# get death info info from HsnBeheer
	try:
		from qx.views import none2empty
		entry = HsnBeheer.objects.using( "mail" ).get( idnr = op_numstr )

		death_location = none2empty( entry.ovlplaats )

		if entry is not None:
			death = { 
				"table_name"     : "HsnBeheer", 
				"edit"           : True, 
				"death_day"      : entry.ovldag, 
				"death_month"    : entry.ovlmnd, 
				"death_year"     : entry.ovljaar, 
				"death_location" : death_location
			}
			print( death )
		else:
			print( "HsnBeheer entry %s does not exist" % op_numstr )

	except:
		print( "hsn_manage/views/get_death_hsnmanage( %s )" % op_numstr)
		type, value, tb = exc_info()
		msg = "HsnBeheer.objects.get failed: %s" % value
		print( "%s\n" % msg )
	
	return death



def get_partners( op_number ):
	"""
	List of partner mentioning of OP in Huwknd and Mail table
	"""
	partners_huwknd = get_partners_huwknd( op_number )
	partners_mail   = get_partners_mail(   op_number )
	
	partners = []
	for partner_huwknd in partners_huwknd:
		partners.append( partner_huwknd[ "fullname" ] )
	
	for partner_mail in partners_mail:
		partner_mail_date = partner_mail[ "mar_date" ]
		
		duplicate = False
		for partner_huwknd in partners_huwknd:
			partner_huwknd_date = partner_huwknd[ "mar_date" ]
			if partner_huwknd_date == partner_mail_date:
				duplicate = True
				break
				
		if not duplicate:
			partners.append( partner_mail[ "name" ] )
	
	return partners



def get_partners_huwknd( op_number ):
	"""
	List of partner mentioning of OP in Huwknd table
	"""
	print( "get_partners_huwknd()" )
	
	npartners = 0
	partners = []
		
	huwknd_qs = get_huwknd( op_number )
	
	if huwknd_qs is None:
		print( "Huwknd does not contain partners for OP %d", op_number )
	else:
		nhuwknds = huwknd_qs.count()
		print( "Huwknd has %d entries for OP %s" % ( nhuwknds, op_number ) )
		for huwknd in huwknd_qs:
			mar_date  = "%02d/%02d/%04d" % ( int(huwknd.hdag), int(huwknd.hmaand), int(huwknd.hjaar) )
			gebsex = huwknd.gebsex
			
			if gebsex == 'm':					# OP is man
				partnersex = 'v'
				familyname = huwknd.anmhv		# familyname wife
				firstname1 = huwknd.vrn1hv		# firstname1 wife
				firstname2 = huwknd.vrn2hv		# firstname2 wife
				firstname3 = huwknd.vrn3hv		# firstname3 wife
			elif gebsex == 'v':					# OP is woman
				partnersex = 'm'
				familyname = huwknd.anmhm		# familyname husband
				firstname1 = huwknd.vrn1hm		# firstname1 husband
				firstname2 = huwknd.vrn2hm		# firstname2 husband
				firstname3 = huwknd.vrn3hm		# firstname3 husband
			
			if familyname is None: familyname = ""
			if firstname1 is None: firstname1 = ""
			if firstname2 is None: firstname2 = ""
			if firstname3 is None: firstname3 = ""
			
			fullname = familyname
			fullname += ", "
			fullname += firstname1
			if firstname2 != "":
				fullname += " "
				fullname += firstname2
			if firstname3 != "":
				fullname += " "	
				fullname += firstname3
				
			if gebsex == 'm' or gebsex == 'v':
				partner = {
					"mar_date" : mar_date,
					"sex"      : partnersex,
					"fullname" : fullname
				}
				npartners += 1
				print( "partner:", partner )
				partners.append( partner )
		print( "Huwknd has %d partner entries for OP %s" % ( npartners, op_number ) )
	
	return partners



def get_partners_mail( op_number ):
	"""
	List of partner mentioning of OP in Mail table
	"""
	print( "get_partners_mail()" )

	npartners = 0
	partners = []
	
	# List of partner mentioning of OP in mails
	try:
		mail_qs = Mail.objects.using( "mail" ).filter( idnr = op_number, type = "HUW" ).order_by( "id" )
		
		if mail_qs is None:
			print( "Mail does not contain partners for OP %d", op_number )
		else:
			nmails = mail_qs.count()
			print( "Mail has %d entries for OP %s" % ( nmails, op_number ) )
			for mail in mail_qs:
				mar_date = normalize_date( mail.datum )
				partner_name = mail.oppartner
				if partner_name is not None:
					npartners += 1
					print( "mar_date:", mar_date, "partner:", partner_name )
					partner = { "mar_date" : mar_date, "name" : partner_name }
					partners.append( partner )
			print( "Mail has %d non-empty partner entries for OP %s" % ( npartners, op_number ) )
			
	except:
		print( "get_partners()" )
		type, value, tb = exc_info()
		msg = "Mail.objects.filter failed: %s" % value
		print( "%s\n" % msg )
	
	return partners



def get_missing( op_numstr ):
	print( "hsn_manage/views/get_missing:", op_numstr )

	missing_data = []

	# get missing data info info from HsnKwyt
	try:
		missing_qs = HsnKwyt.objects.using( "mail" ).filter( idnr = op_numstr ).order_by( "idvolgnr" )

		if missing_qs is not None:
			for entry in missing_qs:
				missing = {
					"id"       : entry.id, 			# AI PK
					"idnr"     : entry.idnr, 
					"idvolgnr" : entry.idvolgnr,  
					"begin_d"  : entry.startdag, 
					"begin_m"  : entry.startmaand, 
					"begin_y"  : entry.startjaar, 
					"end_d"    : entry.eindedag, 
					"end_m"    : entry.eindemaand, 
					"end_y"    : entry.eindejaar, 
					"found"    : entry.gevonden, 
					"reason"   : entry.reden, 
					"location" : entry.locatie
				}
				
				missing_data.append( missing )
		else:
			print( "HsnKwyt entry %s does not exist", op_numstr )

	except:
		print( "hsn_manage/views/get_missing( %s )" % op_numstr)
		type, value, tb = exc_info()
		msg = "HsnKwyt.objects.filter failed: %s" % value
		print( "%s\n" % msg )

	return missing_data



def get_hsnmanage( op_numstr ):
	hsnopmanage = {}
	
	# get hsnmanage info info from HsnBeheer
	phase_a = None
	phase_b = None
	phase_c = None
				
	try:
		hsnmanage_qs = HsnBeheer.objects.using( "mail" ).filter( idnr = op_numstr )

		if hsnmanage_qs is None:
			print( "HsnBeheer entry %s does not exist", op_numstr )
		else:
			from qx.views import none2empty
			
			for hsnmanage in hsnmanage_qs:
				mailtype = hsnmanage.mail_type
				if mailtype is None: mailtype = ""
				
				ovldag  = hsnmanage.ovldag
				ovlmnd  = hsnmanage.ovlmnd
				ovljaar = hsnmanage.ovljaar
				
				if ovldag  == 0: ovldag  = ""
				if ovlmnd  == 0: ovlmnd  = ""
				if ovljaar == 0: ovljaar = ""
				
				ovlplaats = none2empty( hsnmanage.ovlplaats )
				
				phase_a = hsnmanage.fase_a
				phase_b = hsnmanage.fase_b
				phase_c = hsnmanage.fase_c_d
				#print( "phase_a:", phase_a, "phase_b:", phase_b, "phase_c:", phase_c )
        
				hsnopmanage = \
				{
					"invoerstatus" : hsnmanage.invoerstatus,
					"mailtype"     : mailtype,
					"ovldag"       : ovldag,
					"ovlmnd"       : ovlmnd,
					"ovljaar"      : ovljaar,
					"ovlplaats"    : ovlplaats,
					"phase_a"      : phase_a,
					"phase_b"      : phase_b,
					"phase_c"      : phase_c
				}

	except:
		print( "hsn_manage/views/get_hsnmanage( %s )" % op_numstr )
		type, value, tb = exc_info()
		msg = "HsnBeheer.objects.filter failed: %s" % value
		print( "%s\n" % msg )


	# prevent selecting fixed string labels in the client that no longer exist
	print( "phase_a:", phase_a, "phase_b:", phase_b, "phase_c:", phase_c )
	phase_a_str = ""
	try:
		tfasea = TekstFaseA.objects.using( "mail" ).filter( fase_a = hsnmanage.fase_a ).first()
		if tfasea is not None:
			phase_a_str = str( phase_a ) + " - " + tfasea.fase_a_text
	except:
		phase_a = ""
		type, value, tb = exc_info()
		msg = "TekstFaseA.objects failed: %s" % value
		print( "%s\n" % msg )

	phase_b_str = ""
	try:
		tfaseb = TekstFaseB.objects.using( "mail" ).filter( fase_b = hsnmanage.fase_b ).first()
		if tfaseb is not None:
			phase_b_str = str( phase_b ) + " - " + tfaseb.fase_b_text
	except:
		phase_b = ""
		type, value, tb = exc_info()
		msg = "TekstFaseB.objects failed: %s" % value
		print( "%s\n" % msg )
		
	phase_c_str = ""
	try:
		tfasec = TekstFaseCD.objects.using( "mail" ).filter( fase_c_d = hsnmanage.fase_c_d ).first()
		if tfasec is not None:
			phase_c_str = str( phase_c ) + " - " + tfasec.fase_c_d_text
	except:
		phase_c = ""
		type, value, tb = exc_info()
		msg = "TekstFaseCD.objects failed: %s" % value
		print( "%s\n" % msg )
		
	print( "phase_a:", phase_a, "phase_b:", phase_b, "phase_c:", phase_c )
	
	hsnopmanage[ "phase_a_str" ] = phase_a_str
	hsnopmanage[ "phase_b_str" ] = phase_b_str
	hsnopmanage[ "phase_c_str" ] = phase_c_str

	
	# also need the number of the location
	hsnopmanage[ "ovlplaats_gemnr" ] = ""

	location = hsnmanage.ovlplaats
	plaats_qs = get_location_by_gemnaam( location )
	
	if plaats_qs is not None:
		location_num = plaats_qs.gemnr
		hsnopmanage[ "ovlplaats_gemnr" ] = location_num
	else:
		print( "Plaats entry %s does not exist", location )
	
	# also need the voortgang string
	invoerstatus = hsnmanage.invoerstatus
	print( "invoerstatus:", invoerstatus )
	voortgang = get_voortgang( invoerstatus )
	print( "voortgang:", voortgang )
	hsnopmanage[ "statustekst" ] = voortgang
	
	return hsnopmanage



def get_voortgang( invoerstatus ):
	
	voortgang = ""
	
	try:
		voortgang_qs = TekstVoortgang.objects.using( "mail" ).get( invoerstatus = invoerstatus )
		voortgang = voortgang_qs.invoerstatustekst
	except:
		print( "hsn_manage/views/get_voortgang( invoerstatus )" )
		type, value, tb = exc_info()
		msg = "TekstVoortgang.objects failed: %s" % value
		print( "%s\n" % msg )

	return voortgang



def put_hsnmanage( fields ):
	
	status = ""
	
	print( fields )
	idnr = fields.pop( "idnr" )		# pk
	print( "idnr", idnr )
	print( fields )
	for key, value in fields.items():
		print( key, "=", value )
    
	try:
		numrows = HsnBeheer.objects.using( "mail" ).filter( idnr = idnr ).update( **fields )
	except ObjectDoesNotExist:
		# not found
		status = "NOT FOUND"
		print( "put_hsnmanage() OP %s not present in table HsnBeheer" % idnr )
	except:
		# other error
		status = "ERROR"
		print( "hsn_manage/views/put_hsnmanage() OP = %s" % idnr )
		type, value, tb = exc_info()
		msg = "HsnBeheer.objects.update failed: %s" % value
		print( "%s\n" % msg )
	else:
		# no exception
		status = "UPDATED"
		print( "put_hsnmanage() record updated for OP %s in table HsnBeheer" % idnr )
	
	return status



def put_hsnmanagemissing( missing_req ):
	"""
	We assume that the new missing data is complete: 
	Update the HsnKwyt table in 2 steps: 
	1) first we do an update_or_create() for all records received from the client. 
	2) the we delete the records that have no corresponding volgnr in the new list. 
	"""
	
	status = ""
	msg = ""
	
#	print( missing_req )
	
	idnr  = missing_req.get( "idnr" )
	nrows = missing_req.get( "nrows" )
	rdata = missing_req.get( "rdata" )
	print( "idnr:", idnr, "nrows:", nrows )
	
	nupdated = 0
	ncreated = 0
	ndeleted = 0
	
	volgnrs_new = []
	
	# step 1: update and/or create records
	for row in rdata:
	#	print( row )
		idnr     = row.get( "idnr" )
		idvolgnr = row.get( "idvolgnr" )
		
		missing_dict = {
			"startdag"   : row.get( "begin_d" ),
			"startmaand" : row.get( "begin_m" ),
			"startjaar"  : row.get( "begin_y" ),
			"eindedag"   : row.get( "end_d" ),
			"eindemaand" : row.get( "end_m" ),
			"eindejaar"  : row.get( "end_y" ),
			"gevonden"   : row.get( "found" ),
			"reden"      : row.get( "reason" ),
			"locatie"    : row.get( "location" )
		}
		
		try:
			status = "OK"
			obj, created = HsnKwyt.objects.using( "mail" ).update_or_create(
				idnr = idnr, idvolgnr = idvolgnr, defaults = None, **missing_dict )
		#	print( "idnr: %s, idvolgnr: %s, created: %s" % ( idnr, idvolgnr, created ) )
			
			if created: 
				ncreated += 1
			else:
				nupdated += 1
			
			volgnrs_new.append( idvolgnr )
		except:
			status = "ERROR"
			print( "hsn_manage/views/put_hsnmanagemissing() idnr = %s, idvolgnr = %s" % ( idnr, idvolgnr ) )
			type, value, tb = exc_info()
			msg = "HsnKwyt.objects.update_or_create failed: %s" % value
			print( "%s\n" % msg )
			print( missing_dict )
		
	
	# step 2: delete records
	# if the input data is empty, we just delete the existing records for the given OP (idnr)
	try:
		status = "OK"
		if nrows == 0:
			HsnKwyt.objects.using( "mail" ).filter( idnr = idnr ).delete()
		else:
			print( volgnrs_new )
			volgnrs_del = []
			hsnkwyt_qs = HsnKwyt.objects.using( "mail" ).filter( idnr = idnr )
			if hsnkwyt_qs is not None:
				for hsnkwyt in hsnkwyt_qs:
					idvolgnr = hsnkwyt.idvolgnr
					print( idvolgnr )
					if idvolgnr in volgnrs_new:
						print( "keep idvolgnr: %d of OP: %s" % ( idvolgnr, idnr ) )
					else:
						print( "delete idvolgnr: %d of OP: %s" % ( idvolgnr, idnr ) )
						ndeleted += 1
						HsnKwyt.objects.using( "mail" ).filter( idnr = idnr, idvolgnr = idvolgnr ).delete()
	except:
		status = "ERROR"
		print( "hsn_manage/views/put_hsnmanagemissing() idnr = %s, idvolgnr = %s" % ( idnr, idvolgnr ) )
		type, value, tb = exc_info()
		msg = "HsnKwyt.objects.delete failed: %s" % value
		print( "%s\n" % msg )
	
	msg = "put_hsnmanagemissing() idnr = %s, updated: %d, created: %d, deleted: %d" % \
		( idnr, nupdated, ncreated, ndeleted )
	print( msg )
		
	return status, msg

# [eof]
