# -*- coding: utf-8 -*-

"""
Author:		Fons Laan, KNAW IISH - International Institute of Social History
Project:	HSN Mail
Name:		hsnmailenbeheer/urls.py
Version:	1.0.0
Goal:		URL dispatcher

26-May-2015	Created
25-Feb-2016	Login
02-Mar-2016	Logout
02-Mar-2016	Changed
"""

from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from hsnmailenbeheer import settings


urlpatterns = []

if settings.ADMIN_ENABLED:
	urlpatterns += [
		url( r'^admin/', admin.site.urls ),
	]

urlpatterns += [
#	url( r'^accounts/login/$', include( auth_views.login ) ),
#	url( r'^accounts/',        include( 'registration.backends.simple.urls' ) ),	# django-registration

	url( r'',                  include( 'loginout.urls' ) ),
	url( r'',                  include( 'qx.urls' ) ),
]

# [eof]
