# -*- coding: utf-8 -*-

"""
Author:		Fons Laan, KNAW IISH - International Institute of Social History
Project:	HSN Mail
Name:		print.py
Version:	1.0.1
Goal:		Show printers
Notice:		Derived from cupstree; original cupstree code from: 
			/usr/share/doc/python-cups-doc-1.9.63/examples/cupstree.py
			which is from the rpm: python-cups-doc-1.9.63-6.el7.x86_64

17-Jun-2015	Created
20-Mar-2017	Changed
"""

# future-0.16.0 imports for Python 2/3 compatibility
from __future__ import ( absolute_import, division, print_function, unicode_literals )
from builtins import ( ascii, bytes, chr, dict, filter, hex, input, int, list, map, 
    next, object, oct, open, pow, range, round, super, str, zip )
from future.utils import iteritems

from sys import stderr, exc_info
import cups

from hsnmailenbeheer import settings


def getippqueue( dev, queue, depth ): 
	name = dev.rfind ( '/' )
	name = dev[ name + 1: ]
	dev  = dev[ 6: ]
	e    = dev.find( ':' )
	
	if e == -1:
		e = dev.find( '/' )
	host = dev[ :e ]
	cups.setServer( host )
	try:
		c = cups.Connection ()
		printers = c.getPrinters ()
		classes  = c.getClasses ()
	except RuntimeError:
		# Failed to connect.
		return
	except cups.IPPError as e:
		if e == cups.IPP_OPERATION_NOT_SUPPORTED:
			# CUPS-Get-Printers not supported so not a CUPS server.
			printers = {}
			classes  = {}
		else:
			return

	queue = c.getPrinterAttributes( name )
	dev = queue[ 'device-uri' ]
	getqueue( name, queue, host, depth + 1, printers, classes )



def getqueue( name, queue, host, depth, printers, classes ):
	indent = do_indent( depth )
	
	try:
		print( "host:\t%s" % settings.HOST )
	except:
		pass
	
	printer_dict = {}
	
	if queue[ 'printer-type' ] & cups.CUPS_PRINTER_CLASS:
		print( "%s* Name:\t%s[@%s] (class)" % (indent, name, host) )
		
		dev = queue[ 'device-uri' ]
		if dev.startswith( 'ipp:' ):
			getippqueue ( dev, queue, depth )
		else:
			members = classes[ name ]
			depth += 1
			indent = do_indent( depth )
			for member in members:
				getqueue( member, printers[ member ], host, depth, printers, classes )
	else:
		print( "%s* Name:\t%s[@%s]" % (indent, name, host) )
		
		dev  =  queue[ 'device-uri' ]
		info = queue[ 'printer-info' ]
		
		print( "%sURI:\t%s" % (indent, dev) )
		print( "%sInfo:\t%s" % (indent, info) )
		
		if dev.startswith( 'ipp:' ):
			getippqueue( dev, name, depth )

	if depth == 0:
		print

	printer_dict = {
		"host" : host,
		"name" : name, 
		"uri"  : dev,
		"info" : info
	}
	
	return printer_dict



def do_indent( indent ):
	return "  "*indent



def get_printers( host = None, depth = 0 ) :
	if not host:
		try:
			host = settings.HOST
		except:
			host = "localhost"
		
	msg = "OK"
	try:
		cups.setServer( host )
	except:
		print( "cupstree/get_printers( )" )
		type, value, tb = exc_info()
		msg = "cups.setServer() for host %s failed" % host
		print( "%s\n" % msg )
		return { "msg" : msg, "list" : [] }

	printers = None
	classes  = None
	indent   = None
	
	msg = "OK"
	try:
		c = cups.Connection()
		printers = c.getPrinters ()
		classes  = c.getClasses ()
		indent   = do_indent( depth )
	except:
		print( "cupstree/get_printers( )" )
		type, value, tb = exc_info()
		msg = "cups.Connection() for host %s failed" % host
		print( "%s\n" % msg )
		return { "msg" : msg, "list" : [] }
	
	printer_list = []
	try:
		for ( name, queue ) in iteritems( printers ):
			printer_dict = getqueue( name, queue, host, depth, printers, classes )
			printer_list.append( printer_dict )
	except:
		print( "cupstree/get_printers( )" )
		type, value, tb = exc_info()
		msg = "cups getqueue for host %s failed" % host
		print( "%s\n" % msg )
	
	return { "msg" : msg, "list" : printer_list }

# [eof]
