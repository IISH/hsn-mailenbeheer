# -*- coding: utf-8 -*-

"""
Author:		Fons Laan, KNAW IISH - International Institute of Social History
Project:	HSN Mail
Name:		urls.py
Version:	1.0.0
Goal:		

09-Jun-2015	Created
24-Feb-2016	Changed
"""

from django.conf.urls import patterns

from .views import ( login, gethsndata, gethsnopdata, puthsnmanage, puthsnmanagemissing, 
	putmailbev, putmailhuw, putmailbevreceived, putopmutation, printmailbev )


urlpatterns = patterns( '',
	( r'gethsndata/',          gethsndata ),
	( r'gethsnopdata',         gethsnopdata ),		# no trailing /
	( r'puthsnmanage/',        puthsnmanage ),
	( r'puthsnmanagemissing/', puthsnmanagemissing ),
	( r'putmailbev/',          putmailbev ),
	( r'putmailhuw/',          putmailhuw ),
	( r'putmailbevreceived/',  putmailbevreceived  ),
	( r'putopmutation/',       putopmutation ),
	( r'printmailbev/',        printmailbev ),
	
#	( r'', gethsndata ),		# default action
	( r'', login ),			  	# default action
)

# [eof]
