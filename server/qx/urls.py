# -*- coding: utf-8 -*-

"""
Author:		Fons Laan, KNAW IISH - International Institute of Social History
Project:	HSN Mail
Name:		urls.py
Version:	1.0.0
Goal:		

09-Jun-2015	Created
02-Mar-2016	Changed
"""

from django.conf.urls import url

from .views import ( gethsndata, gethsnopdata, puthsnmanage, puthsnmanagemissing, 
	putmailbev, putmailhuw, putmailbevreceived, putopmutation, printmailbev )


urlpatterns = [
	url( r'gethsndata/',          gethsndata ),
	url( r'gethsnopdata',         gethsnopdata ),		# no trailing /
	url( r'puthsnmanage/',        puthsnmanage ),
	url( r'puthsnmanagemissing/', puthsnmanagemissing ),
	url( r'putmailbev/',          putmailbev ),
	url( r'putmailhuw/',          putmailhuw ),
	url( r'putmailbevreceived/',  putmailbevreceived  ),
	url( r'putopmutation/',       putopmutation ),
	url( r'printmailbev/',        printmailbev ),
	
#	url( r'', gethsndata ),		# default action
]

# [eof]
