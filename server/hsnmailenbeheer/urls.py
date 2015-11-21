# -*- coding: utf-8 -*-

"""
Author:		Fons Laan, KNAW IISH - International Institute of Social History
Project:	HSN Mail
Name:		urls.py
Version:	1.0.0
Goal:		URL dispatcher

26-May-2015	Created
17-Nov-2015	Changed
"""

from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from hsnmailenbeheer import settings

urlpatterns = [
#	url( r'^accounts/',        include( 'registration.backends.simple.urls' ) ),
#	url( r'^accounts/login/$', auth_views.login ),
	url( r'',                  include( 'qx.urls' ) ),
]

if settings.ADMIN_ENABLED:
	urlpatterns += patterns( '',
		( r'^admin/(.*)', include( admin.site.urls ) ),
	)

# [eof]
