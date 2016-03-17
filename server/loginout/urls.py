# -*- coding: utf-8 -*-

"""
Author:		Fons Laan, KNAW IISH - International Institute of Social History
Project:	HSN Mail
Name:		loginout/urls.py
Version:	1.0.0
Goal:		urls

02-Mar-2016	Created
16-Mar-2016	Changed
"""

from django.conf.urls import url

from .views import ( hsn_login, hsn_logout )


urlpatterns = [
	url( r'login',  hsn_login ),		# no trailing /
	url( r'logout', hsn_logout ),		# no trailing /
	
#	url( r'', login ),			  		# default action
]

# [eof]
