# -*- coding: utf-8 -*-

"""
Author:		Fons Laan, KNAW IISH - International Institute of Social History
Project:	HSN Mail
Name:		print.py
Version:	1.0.1
Goal:		Send letters to printer
Notice:		A PostScript letter is created, saved, and sent trough CUPS to the default printer

Functions:
def print_mailbev():
def get_mailtype( idnr ):
def get_archive( gemnr ):
def get_pathname_psfile( id ):
def create_ps_letter( pathname_print_out, OP ):
def print_ps_line( psfile, string, d, x, y ):
def print_ps_letter( id, pathname_print_out ):
def update_status( id ):

17-Jun-2015	Created
08-Mar-2016	Split-off hsn_central & hsn_reference db's
16-Dec-2016	Letter contents changed
22-Mar-2017 Changed
"""

# future-0.16.0 imports for Python 2/3 compatibility
from __future__ import ( absolute_import, division, print_function, unicode_literals )
from builtins import ( ascii, bytes, chr, dict, filter, hex, input, int, list, map, 
    next, object, oct, open, pow, range, round, super, str, zip )

import os.path
from sys import stderr, exc_info
from sys import path
import datetime

import codecs
import cups

from django.conf import settings
from hsnmailenbeheer import settings
from mail.models import ArchiefGemeente, HsnBeheer, Mail
from reference.views import get_opsex
from op_select.op import get_op_info
	
from .cupstree import get_printers

debug = settings.DEBUG

# now from settings_local
#ID_IN_FN = True		# mail pk id in ps filename
#DO_PRINT = True		# print the PostScript letter files

maxcharsline = 90
basename_print = "letter-bev"

MAIL_PRINT_DIR_DEFAULT       = "/tmp"
MAIL_ADD_ID_TO_FN_DEFAULT    = True
MAIL_SENT_TO_PRINTER_DEFAULT = True
MAIL_UPDATE_TABLE_DEFAULT    = True


def print_mailbev():
	if debug: print( "mail/print/print_mailbev(" )
	
	# notice, no cups.py, but just a .cups.so
	#print( os.path.abspath( cups.__file__ ) )
	# .../python2710/lib/python2.7/site-packages/cups.so
	
	ids = []
	
	try:
		from qx.views import none2empty
		
		ret_status = "OK"
		msg = ""
	#	mail_qs = Mail.objects.using( "mail" ).filter( status = 0, type = "BEV" ).order_by( "provnr", "archiefnaam", "id" )	# "provnr" not in Mail table
	#	mail_qs = Mail.objects.using( "mail" ).filter( status = 0, type = "BEV" ).order_by( "archiefnaam", "id" )	# "archiefnaam" not in Mail table
		mail_qs = Mail.objects.using( "mail" ).filter( status = 0, type = "BEV" ).order_by( "gemnr", "id" )
		
		if mail_qs is None:
			msg = "Mail does not contain entries with status = 0"
			if debug: print( msg )
		else:
			nmails_bev = mail_qs.count()
			if debug: print( "Number of mails with status = 0:", nmails_bev )
			
			for mail in mail_qs:
				if debug: print( mail )
				id = str( mail.id )
				ids.append( id )
				
				opsex    = none2empty( get_opsex(    mail.idnr ) )
				mailtype = none2empty( get_mailtype( mail.idnr ) )
				if debug: print( "opsex:", opsex, ", mailtype:", mailtype )
				
				archive = none2empty( get_archive( mail.gemnr ) )
				if debug: print( "archive:", archive )
				
				info_list = none2empty( get_op_info( mail.idnr ) )
				if debug: print( "info_list:", info_list )
				
				pathname_psfile = get_pathname_psfile( mail.gemnr, id )
				
				OP = {
					"info_list"   : info_list,
					"mailtype"    : mailtype,
					"idnr"        : str( mail.idnr ),
					"kind"        : none2empty( mail.aard ),
					"gemnr"       : mail.gemnr,
					"archive"     : archive,
					"datum"       : none2empty( mail.datum ),
					"periode"     : none2empty( mail.periode ),
					"naamgem"     : none2empty( mail.naamgem ),
					"opmerk"      : none2empty( mail.opmerk ),
					"opsex"       : opsex,
					"opident"     : none2empty( mail.opident ),
					"oppartner"   : none2empty( mail.oppartner ),
					"opvader"     : none2empty( mail.opvader ),
					"opmoeder"    : none2empty( mail.opmoeder ),
					"infoouders"  : none2empty( mail.infoouders ),
					"infopartner" : none2empty( mail.infopartner ),
					"inforeis"    : none2empty( mail.inforeis )
				}
				
				create_ps_letter( pathname_psfile, OP )
				
				try:
					MAIL_SENT_TO_PRINTER = settings.MAIL_SENT_TO_PRINTER
				except:
					MAIL_SENT_TO_PRINTER = MAIL_SENT_TO_PRINTER_DEFAULT
				
				try:
					MAIL_UPDATE_TABLE = settings.MAIL_UPDATE_TABLE
				except:
					MAIL_UPDATE_TABLE = MAIL_UPDATE_TABLE_DEFAULT
		
				if MAIL_SENT_TO_PRINTER:
					ret_status, msg = print_ps_letter( id, pathname_psfile )
					
					if ret_status == "OK" and MAIL_UPDATE_TABLE:
						update_status_date( id )
				else:
					if MAIL_UPDATE_TABLE:
						update_status_date( id )
				
			#	break	# test: create/print only 1 letter

	except:
		ret_status = "ERROR"
		print( "print_mailbev()" )
		type, value, tb = exc_info()
		msg = "Mail.objects.filter failed: %s" % value
		print( "%s\n" % msg )
	
	return ret_status, msg, ids



def get_mailtype( idnr ):
	mail_type = None
	# get mailtype from HsnBeheer
	try:
		hsnmanage = HsnBeheer.objects.using( "mail" ).get( idnr = idnr )
		if hsnmanage is not None:
			mail_type = hsnmanage.mail_type
	except:
		print( "print/get_mailtype()" )
		type, value, tb = exc_info()
		msg = "HsnBeheer.objects.get failed: %s" % value
		print( "%s\n" % msg )

	return mail_type



def get_archive( gemnr ):
	archiefnaam = ""
	gemeentemet = ""
	archive = ""
	
	# get archive from ArchiefGemeente
	try:
		archive_info = ArchiefGemeente.objects.using( "mail" ).get( gemnr = gemnr )
		if archive_info is not None:
			archiefnaam = archive_info.archiefnaam
			gemeentemet = archive_info.gemeente_met_archief
			
			if archiefnaam is None: archiefnaam = ""
			if gemeentemet is None: gemeentemet = ""
	except:
		print( "print/get_archive()" )
		type, value, tb = exc_info()
		msg = "ArchiefGemeente.objects.get failed: %s" % value
		print( "%s\n" % msg )
	
	if archiefnaam == "":
		archive = gemeentemet
	else:
		archive = archiefnaam
	
	return archive



def get_pathname_psfile( gemnr, id ):
	if debug: print( "get_pathname_psfile()" )
	
	try:
		MAIL_PRINT_DIR = settings.MAIL_PRINT_DIR
	except:
		MAIL_PRINT_DIR = MAIL_PRINT_DIR_DEFAULT
	if debug: print( "MAIL_PRINT_DIR:", MAIL_PRINT_DIR )
	
	basename_psfile = basename_print
	
	try:
		MAIL_ADD_ID_TO_FN = settings.MAIL_ADD_ID_TO_FN
	except:
		MAIL_ADD_ID_TO_FN = MAIL_ADD_ID_TO_FN_DEFAULT
	
	if MAIL_ADD_ID_TO_FN and id:
		basename_psfile += "-gemnr="
		basename_psfile += str( gemnr )
		basename_psfile += "-id="
		basename_psfile += id
		
	
	filename_psfile = basename_psfile + ".ps"
	if debug: print( filename_psfile )
	pathname_psfile = os.path.join( MAIL_PRINT_DIR, filename_psfile )
	if debug: print( pathname_psfile )

	return pathname_psfile



def create_ps_letter( pathname_print_out, OP ):
	"""
	Create a PostScript file with the letter contents for a given OP
	"""
	if debug: print( "create_ps_letter()" )
	
	try:
		if debug: print( "open:", pathname_print_out )
		printps_file = codecs.open( pathname_print_out, 'wb', "latin-1" )
	except:
		status = "ERROR"
		print( "mail/views/create_ps_letter()" )
		type, value, tb = exc_info()
		msg = "Opening PostScript letter failed: %s" % value
		print( "%s\n" % msg )
		return status, msg

	info_list   = OP.get( "info_list" )
	mailtype    = OP.get( "mailtype" )
	idnr        = OP.get( "idnr" )
	kind        = OP.get( "kind" )
	gemnr       = OP.get( "gemnr" )
	archive     = OP.get( "archive" )
	datum       = OP.get( "datum" )
	periode     = OP.get( "periode" )
	naamgem     = OP.get( "naamgem" )
	opmerk      = OP.get( "opmerk" )
	opsex       = OP.get( "opsex" )
	opident     = OP.get( "opident" )
	oppartner   = OP.get( "oppartner" )
	opvader     = OP.get( "opvader" )
	opmoeder    = OP.get( "opmoeder" )
	infoouders  = OP.get( "infoouders" )
	infopartner = OP.get( "infopartner" )
	inforeis    = OP.get( "inforeis" )
	
	if len( opident ) > 0 and opident[ -1 ] != '.': opident += '.'
	
	if infoouders == 1:
		infoouders = True
	else:
		infoouders = False
	
	if infopartner == 1:
		infopartner = True
	else:
		infopartner = False
	
	if debug: 
		print( "mailtype:   ", mailtype   .encode( 'utf8' ) )
		print( "kind:       ", kind       .encode( 'utf8' ) )
		print( "gemnr:      ", gemnr )
		print( "archive:    ", archive    .encode( 'utf8' ) )
		print( "datum:      ", datum      .encode( 'utf8' ) )
		print( "periode:    ", periode    .encode( 'utf8' ) )
		print( "naamgem:    ", naamgem    .encode( 'utf8' ) )
		print( "opmerk:     ", opmerk     .encode( 'utf8' ) )
		print( "opsex:      ", opsex      .encode( 'utf8' ) )
		print( "opident:    ", opident    .encode( 'utf8' ) )
		print( "oppartner:  ", oppartner  .encode( 'utf8' ) )
		print( "opvader:    ", opvader    .encode( 'utf8' ) )
		print( "opmoeder:   ", opmoeder   .encode( 'utf8' ) )
		print( "infoouders: ", infoouders )		# bool
		print( "infopartner:", infopartner )	# bool
		print( "inforeis:   ", inforeis )		# bool
	
	# PostScript units: 
	# 72 points for an inch, 28.3465 points for a cm
	# origin is lower left corner
	x = 90		# left margin
	tab = 40	# added to x
#	y = vertical position
	d = 13		# line spacing for 11 point font
	
	
	month_names = [ "januari", "februari", "maart", "april", "mei", "juni", 
		"juli", "augustus", "september", "oktober", "november", "december" ]
	
	now = datetime.datetime.now()
	date_str = "%s %s %s" % ( now.day, month_names[ now.month-1 ], now.year )
	#if debug: print( date_str )
	
	try:
		printps_file.write( "%!PS\n\n" )

		"""
		# To support the Euro symbols € and the French o-e ligatures Œ and œ, 
		# ISO latin-9 (ISO/IEC 8859-15) encoding is needed. 
		# Since ISOLatin9Encoding is not predefined, it must be set explicitely: 
		
		printps_file.write( "/ISOLatin9Encoding [\n" )
		printps_file.write( " /.notdef /.notdef /.notdef /.notdef /.notdef /.notdef /.notdef /.notdef\n" )
		printps_file.write( " /.notdef /.notdef /.notdef /.notdef /.notdef /.notdef /.notdef /.notdef\n" )
		printps_file.write( " /.notdef /.notdef /.notdef /.notdef /.notdef /.notdef /.notdef /.notdef\n" )
		printps_file.write( " /.notdef /.notdef /.notdef /.notdef /.notdef /.notdef /.notdef /.notdef\n" )
		printps_file.write( " /space /exclam /quotedbl /numbersign /dollar /percent /ampersand\n" )
		printps_file.write( " /quoteright /parenleft /parenright /asterisk /plus /comma /minus\n" )
		printps_file.write( " /period /slash /zero /one /two /three /four /five /six /seven /eight\n" )
		printps_file.write( " /nine /colon /semicolon /less /equal /greater /question /at /A /B /C /D\n" )
		printps_file.write( " /E /F /G /H /I /J /K /L /M /N /O /P /Q /R /S /T /U /V /W /X /Y /Z\n" )
		printps_file.write( " /bracketleft /backslash /bracketright /asciicircum /underscore\n" )
		printps_file.write( " /quoteleft /a /b /c /d /e /f /g /h /i /j /k /l /m /n /o /p /q /r /s /t\n" )
		printps_file.write( " /u /v /w /x /y /z /braceleft /bar /braceright /asciitilde /.notdef\n" )
		printps_file.write( " /.notdef /.notdef /.notdef /.notdef /.notdef /.notdef /.notdef /.notdef\n" )
		printps_file.write( " /.notdef /.notdef /.notdef /.notdef /.notdef /.notdef /.notdef /.notdef\n" )
		printps_file.write( " /dotlessi /grave /acute /circumflex /tilde /macron /breve /dotaccent\n" )
		printps_file.write( " /dieresis /.notdef /ring /cedilla /.notdef /hungarumlaut /ogonek /caron\n" )
		printps_file.write( " /space /exclamdown /cent /sterling /Euro /yen /Scaron /section /scaron\n" )
		printps_file.write( " /copyright /ordfeminine /guillemotleft /logicalnot /hyphen /registered\n" )
		printps_file.write( " /macron /degree /plusminus /twosuperior /threesuperior /Zcaron /mu\n" )
		printps_file.write( " /paragraph /periodcentered /zcaron /onesuperior /ordmasculine\n" )
		printps_file.write( " /guillemotright /OE /oe /Ydieresis /questiondown /Agrave /Aacute\n" )
		printps_file.write( " /Acircumflex /Atilde /Adieresis /Aring /AE /Ccedilla /Egrave /Eacute\n" )
		printps_file.write( " /Ecircumflex /Edieresis /Igrave /Iacute /Icircumflex /Idieresis /Eth\n" )
		printps_file.write( " /Ntilde /Ograve /Oacute /Ocircumflex /Otilde /Odieresis /multiply\n" )
		printps_file.write( " /Oslash /Ugrave /Uacute /Ucircumflex /Udieresis /Yacute /Thorn\n" )
		printps_file.write( " /germandbls /agrave /aacute /acircumflex /atilde /adieresis /aring /ae\n" )
		printps_file.write( " /ccedilla /egrave /eacute /ecircumflex /edieresis /igrave /iacute\n" )
		printps_file.write( " /icircumflex /idieresis /eth /ntilde /ograve /oacute /ocircumflex\n" )
		printps_file.write( " /otilde /odieresis /divide /oslash /ugrave /uacute /ucircumflex\n" )
		printps_file.write( " /udieresis /yacute /thorn /ydieresis\n" )
		printps_file.write( "] def\n" )
		printps_file.write( "\n" )
		
		# re-encode the used fonts
		printps_file.write( "/Times-Roman             /Times-RomanLatin9             ISOLatin9Encoding ReEncode\n" )
		printps_file.write( "/Times-Roman-Oblique     /Times-RomanLatin9-Oblique     ISOLatin9Encoding ReEncode\n" )
		printps_file.write( "/Times-Roman-Bold        /Times-RomanLatin9-Bold        ISOLatin9Encoding ReEncode\n" )
		printps_file.write( "/Times-Roman-BoldOblique /Times-RomanLatin9-BoldOblique ISOLatin9Encoding ReEncode\n" )
		printps_file.write( "\n" )
		
		# select the default font
		printps_file.write( "/Times-RomanLatin9 findfont\n" )
		printps_file.write( "11 scalefont\n" )
		printps_file.write( "setfont\n\n" )
		printps_file.write( "\n" )
		
		"""
		
		# ISO latin-1 (ISO/IEC 8859-1) encoding 
		# re-encode from 7-bit to 8-bit to create room for diacritics
		printps_file.write( "/ReEncode { % inFont outFont encoding | -\n" )
		printps_file.write( "   /MyEncoding exch def\n" )
		printps_file.write( "   exch findfont\n" )
		printps_file.write( "   dup length dict\n" )
		printps_file.write( "   begin\n" )
		printps_file.write( "      {def} forall\n" )
		printps_file.write( "      /Encoding MyEncoding def\n" )
		printps_file.write( "      currentdict\n" )
		printps_file.write( "   end\n" )
		printps_file.write( "   definefont\n" )
		printps_file.write( "} def\n" )
		printps_file.write( "\n" )
		
		# re-encode the used fonts
		printps_file.write( "/Times-Roman             /Times-RomanLatin1             ISOLatin1Encoding ReEncode\n" )
		printps_file.write( "/Times-Roman-Oblique     /Times-RomanLatin1-Oblique     ISOLatin1Encoding ReEncode\n" )
		printps_file.write( "/Times-Roman-Bold        /Times-RomanLatin1-Bold        ISOLatin1Encoding ReEncode\n" )
		printps_file.write( "/Times-Roman-BoldOblique /Times-RomanLatin1-BoldOblique ISOLatin1Encoding ReEncode\n" )
		printps_file.write( "\n" )
				   
		# select font
		printps_file.write( "/Times-RomanLatin1 findfont\n" )
		printps_file.write( "11 scalefont\n" )
		printps_file.write( "setfont\n\n" )
		printps_file.write( "\n" )
		
		"""
		# Alternative re-encoding; i did not try it
		/Courier findfont               % load the font, for instance, Courier
		0 dict copy begin               % copy it to a new dictionary
		/Encoding ISOLatin1Encoding def % replace encoding vector
		/MyCourier /FontName def        % replace font name
		currentdict end
		dup /FID undef                  % remove internal data
		/MyCourier exch definefont pop  % define the new font
		"""
		
		# select big bold font
		printps_file.write( "/Courier-Bold findfont\n" )
		printps_file.write( "20 scalefont\n" )
		printps_file.write( "setfont\n\n" )
		printps_file.write( "\n" )
		
		y = 750
		printps_file.write( str( x + 380 ) + " " + str( y ) + " moveto\n" )
		printps_file.write( "(" + mailtype + ") show\n" )
		
		printps_file.write( str( x + 400 ) + " " + str( y ) + " moveto\n" )
		printps_file.write( "(" + idnr + ") show\n" )
		
		# select default font
		printps_file.write( "/Times-RomanLatin1 findfont\n" )
		printps_file.write( "12 scalefont\n" )
		printps_file.write( "setfont\n\n" )
		printps_file.write( "\n" )
		
		y = 700
		printps_file.write( str( x ) + " " + str( y ) + " moveto\n" )
		printps_file.write( "(Datum print:) show\n" )
		printps_file.write( str( x + 80 ) + " " + str( y ) + " moveto\n" )
		printps_file.write( "(" + date_str + ") show\n" )
		
		y -= d
		printps_file.write( str( x ) + " " + str( y ) + " moveto\n" )
		printps_file.write( "(Archief:) show\n" )
		
		printps_file.write( str( x + 80 ) + " " + str( y ) + " moveto\n" )
		printps_file.write( "(" + archive + ") show\n" )
		
		y = 650
		printps_file.write( str( x ) + " " + str( y ) + " moveto\n" )
		printps_file.write( "(Wij zijn op zoek naar gegevens van de volgende persoon:) show\n" )
		
		y -= (2 * d)
		printps_file.write( str( x + tab ) + " " + str( y ) + " moveto\n" )
		opident = opident.replace( '-', '\255' )		# minus sign -> hyphen: \uad (utf8), 0255 (octal), 173
		printps_file.write( "(" + opident + ") show\n" )
		
		if debug: print( "info_list length:", len( info_list ) )
		if len( info_list ) > 1:
			y -= (2 * d)
			printps_file.write( str( x ) + " " + str( y ) + " moveto\n" )
			printps_file.write( "(" + "Let op! Er zijn veranderingen in de identiteitsgegevens:" + ") show\n" )
			for info in info_list:
				if debug: print( "info:", info )
				id_origin = info.get( "id_origin" )
				if int( id_origin ) != 10:
					display_str = info.get( "display_str" )
					display_str = display_str.replace( '-', '\255' )	# minus sign -> hyphen: \uad (utf8), 0255 (octal), 173
					valid_date  = info.get( "valid_date" )
					y -= d
					printps_file.write( str( x ) + " " + str( y ) + " moveto\n" )
					if valid_date == "//":
						printps_file.write( "(- datum onbekend:) show\n" )
					else:
						printps_file.write( "(- per " + valid_date + ":) show\n" )
					printps_file.write( str( x + 100 ) + " " + str( y ) + " moveto\n" )
					printps_file.write( "(" + display_str + ") show\n" )
		
		y -= (2 * d)
		printps_file.write( str( x ) + " " + str( y ) + " moveto\n" )
	#	printps_file.write( "(Graag zouden wij een kopie ontvangen van de bevolkingsregisters en/of gezinskaarten waarop) show\n" )
		printps_file.write( "(Graag zouden wij een kopie ontvangen van alle pagina's van de bevolkingsregisters) show\n" )
		y -= d
		printps_file.write( str( x ) + " " + str( y ) + " moveto\n" )
		printps_file.write( "(en/of gezinskaarten waarop deze persoon voorkomt voor de periode en gemeente zoals) show\n" )
		y -= d
		printps_file.write( str( x ) + " " + str( y ) + " moveto\n" )
		printps_file.write( "(hieronder genoemd.) show\n" )
		
		y -= (2 * d)
		printps_file.write( str( x ) + " " + str( y ) + " moveto\n" )

		# minus sign -> hyphen: \uad (utf8), 0255 (octal), 173
		datum   = datum  .replace( '-', '\255' )
		periode = periode.replace( '-', '\255' )
		
					
		if kind == 'H':
			s  = "De genoemde persoon vertrok op " + datum + " uit de gemeente " + naamgem
			s += "; graag kopieën van inschrijvingen vanaf het moment van vertrek (hier dus terugzoeken in de tijd!)."
			y = print_ps_line( printps_file, s, d, x, y )
			
		elif kind == 'V':
			s  = "De genoemde persoon kwam aan op " + datum + " in de gemeente " + naamgem
			s += "; graag kopieën van inschrijvingen vanaf het moment van aankomst."
			y = print_ps_line( printps_file, s, d, x, y )

		elif kind == 'B':
			s  = "De genoemde persoon verbleef gedurende de periode " + periode + " in de gemeente " + naamgem
			s += "; graag kopieën van inschrijvingen in deze periode."
			y = print_ps_line( printps_file, s, d, x, y )
		
		
		y -= (2 * d)
		printps_file.write( str( x ) + " " + str( y ) + " moveto\n" )
		printps_file.write( "(Ter informatie:) show\n" )

		if inforeis == 1:
			#if debug: print( "inforeis 1" )
			y -= d
			printps_file.write( str( x ) + " " + str( y ) + " moveto\n" )
			printps_file.write( "(Deze persoon reisde alleen.) show\n" )
			
			if infoouders and infopartner:
				if not (opvader == "" and opmoeder == ""):
					s = "Info "
					if opvader != "" and opmoeder == "":
						s += "vader: " + opvader
					elif opvader == "" and opmoeder != "":
						s += "moeder: "+ opmoeder
					else:
						s += "ouders: " + opvader
						s += " en " + opmoeder
					s += "."
					
					y -= d
					printps_file.write( str( x ) + " " + str( y ) + " moveto\n" )
					y = print_ps_line( printps_file, s, d, x, y )

				if oppartner != "":
					if opsex == 'm':
						s = "Info zijn echtgenote: " + oppartner + "."
					elif opsex == 'v':
						s = "Info haar echtgenoot: " + oppartner + "."
					else:
						s += "zijn/haar echtgeno(o)t(e): " + oppartner
					y -= d
					printps_file.write( str( x ) + " " + str( y ) + " moveto\n" )
					y = print_ps_line( printps_file, s, d, x, y )
				
			elif infoouders and not (opvader == "" and opmoeder == ""):
				s = "Info "
				if opvader != "" and opmoeder == "":
					s += "vader: " + opvader
				elif opvader == "" and opmoeder != "":
					s += "moeder: "+ opmoeder
				else:
					s += "ouders: " + opvader
					s += " en " + opmoeder
				s += "."
				
				y -= d
				printps_file.write( str( x ) + " " + str( y ) + " moveto\n" )
				y = print_ps_line( printps_file, s, d, x, y )
					
			elif infopartner and oppartner != "":
				if opsex == 'm':
					s = "Info zijn echtgenote: " + oppartner + "."
				elif opsex == 'v':
					s = "Info haar echtgenoot: " + oppartner + "."
				else:
						s += "zijn/haar echtgeno(o)t(e): " + oppartner
				y -= d
				printps_file.write( str( x ) + " " + str( y ) + " moveto\n" )
				y = print_ps_line( printps_file, s, d, x, y )
			
		elif inforeis == 2:
			#if debug: print( "inforeis 2" )
			if oppartner != "":
				s = "Deze persoon reisde met "
				if opsex == 'm':
					s += "zijn echtgenote: " + oppartner
				elif opsex == 'v':
					s += "haar echtgenoot: " + oppartner
				else:
					s += "zijn/haar echtgeno(o)t(e): " + oppartner
				s += "."
				
				y -= d
				printps_file.write( str( x ) + " " + str( y ) + " moveto\n" )
				y = print_ps_line( printps_file, s, d, x, y )
		
		elif inforeis == 3:
			#if debug: print( "inforeis 3" )
			if opvader != "" or opmoeder != "":
				s = "Deze persoon reisde met "
				if opsex == 'm':
					s += "zijn "
				elif opsex == 'v':
					s += "haar "
				else:
					s += "zijn/haar : "
				
				if opvader != "" and opmoeder == "":
					s += "vader: " + opvader
				elif opvader == "" and opmoeder != "":
					s += "moeder: "+ opmoeder
				else:
					s += "ouders: " + opvader
					s += " en " + opmoeder
				s += "."
				
				y -= d
				printps_file.write( str( x ) + " " + str( y ) + " moveto\n" )
				y = print_ps_line( printps_file, s, d, x, y )
		
		
		if opmerk is not None and opmerk != "":
			y -= (2 * d)
			printps_file.write( str( x ) + " " + str( y ) + " moveto\n" )
			printps_file.write( "(Overige informatie:) show\n" )
			
			y -= d
			printps_file.write( str( x ) + " " + str( y ) + " moveto\n" )
			
			s  = opmerk
			y = print_ps_line( printps_file, s, d, x, y )
		
		y -= (2 * d)
		printps_file.write( str( x ) + " " + str( y ) + " moveto\n" )
		printps_file.write( "(Ruimte voor uw opmerkingen:) show\n" )
		
		
		# select a bit smaller font for footer
		printps_file.write( "/Times-RomanLatin1 findfont\n" )
		printps_file.write( "11 scalefont\n" )
		printps_file.write( "setfont\n\n" )
		printps_file.write( "\n" )
		
		y = 70
		printps_file.write( "\n" )
		printps_file.write( str( x ) + " " + str( y ) + " moveto\n" )
		printps_file.write( "(Historische Steekproef Nederlandse bevolking (HSN)) show\n" )
		y -= d
		printps_file.write( str( x ) + " " + str( y ) + " moveto\n" )
		printps_file.write( "(Internationaal Instituut voor Sociale Geschiedenis (IISG)) show\n" )
		y -= d
		printps_file.write( str( x ) + " " + str( y ) + " moveto\n" )
		printps_file.write( "(Cruquiusweg 31, 1019 AT Amsterdam, Tel: 020\2556685866, E\255mail: hsn@iisg.nl) show\n" )
		s = "(Cruquiusweg 31, 1019 AT Amsterdam, Tel: 020-6685866, E-mail: hsn@iisg.nl) show\n" 
		s = s.replace( '-', '\255' )		# minus sign -> hyphen: \uad (utf8), 0255 (octal), 173
 
		printps_file.write( "showpage\n" )
	except:
		status = "ERROR"
		print( "mail/views/do_print_mailbev()" )
		type, value, tb = exc_info()
		msg = "Writing PostScript letter failed: %s" % value
		print( "%s\n" % msg )
		return status, msg
	
	try:
		if debug: print( "close:", pathname_print_out )
		printps_file.close()
	except:
		status = "ERROR"
		print( "mail/views/do_print_mailbev()" )
		type, value, tb = exc_info()
		msg = "Closing PostScript letter failed: %s" % value
		print( "%s\n" % msg )
		return status, msg



def print_ps_line( psfile, string, d, x, y ):
	"""
	Simplistic line breaking trhat ignores font size altogether. 
	We use 12 points as default.
	"""

	if debug: print( "print_ps_line()" )
#	print( string.encode( 'utf8' ) )
	
	# minus sign -> hyphen: \uad (utf8), 0255 (octal), 173
	string = string.replace( '-', '\255' )
	
	string = string.replace( "(", "\(" )
	string = string.replace( ")", "\)" )
	if debug: print( string.encode( 'utf8' ) )
	
	psfile.write(  str( x ) + " " + str( y ) + " moveto\n" )
	words = string.split( ' ' )
	
	piece = ""
	length = 0
	for word in words:
	#	print( word.encode( 'utf8' ) )
		if length + len( word ) + 1 > maxcharsline:
			if debug: print( "piece:", piece.encode( 'utf8' ) )
			psfile.write( "(" + piece + ") show\n" )
			# new line
			y -= d
			psfile.write(  str( x ) + " " + str( y ) + " moveto\n" )
			piece = word + " "
			length = len( word ) + 1
		else:
			piece  += word + " "
			length += len( word ) + 1
		
	if debug: print( "piece:", piece.encode( 'utf8' ) )
	psfile.write( "(" + piece + ") show\n" )
	if debug: print( "print_ps_line)(" )
		
	return y



def print_ps_letter( id, pathname_print_out ):
	if debug: print( "print_ps_letter()" )
	status = ""
	msg = ""
			
	try:
		try:
			MAIL_SENT_TO_PRINTER = settings.MAIL_SENT_TO_PRINTER
		except:
			MAIL_SENT_TO_PRINTER = MAIL_SENT_TO_PRINTER_DEFAULT
		
		if MAIL_SENT_TO_PRINTER:
			status = "OK"
			msg = ""
			
			cups_con = cups.Connection ()
			printer = cups_con.getDefault()
			
			title = "HSN print letter"
			if id:
				title += " "
				title += id

			options = {}
			if debug: print( "print to:", printer, ", file:", pathname_print_out )
			cups_con.printFile( printer, pathname_print_out, title, options );
		else:
			status = ""
			msg = "Printing skipped"
	except:
		status = "ERROR"
		print( "print_ps_letter()" )
		type, value, tb = exc_info()
		msg = "Printing failed: %s" % value
		print( "%s\n" % msg )
		return status, msg

	return status, msg



def update_status_date( id ):
	if debug: print( "update_status() id: ", id )
	ret_status = ""
	msg = ""
	
	now = datetime.datetime.now()
	date_str = "%s-%s-%s" % ( now.day, now.month, now.year )
	#if debug: print( date_str )

	fields = { 
		"status"     : 1 ,				# printed: status 0 -> 1
		"printdatum" : date_str
	}
	
	try:
		numrows = Mail.objects.using( "mail" ).filter( id = id ).update( **fields )
	except ObjectDoesNotExist:
		# not found
		ret_status = "NOT FOUND"
		if debug: print( "update_status() id %s not present in table Mail" % id )
	except:
		ret_status = "ERROR"
		print( "update_status(), id: ", id )
		type, value, tb = exc_info()
		msg = "Updating mail status failed: %s" % value
		print( "%s\n" % msg )
		return status, msg
	
	return ret_status, msg

# [eof]
