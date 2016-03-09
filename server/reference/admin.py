# -*- coding: utf-8 -*-

"""
Author:		Fons Laan, KNAW IISH - International Institute of Social History
Project:	HSN Mail
Name:		admin.py
Version:	1.0.0
Goal:		Admin classes for the hsn_central tables

08-Mar-2016	Created
08-Mar-2016	Changed
"""


from django.contrib import admin

from .models import ( Hsnrp, Plaats )


class HsnrpAdmin( admin.ModelAdmin ):
	list_display = ( 'id', 'idnr', 'id_origin', 'project', 'gemnr', 'valid_day', 'valid_month', 'valid_year', 'rp_family', 
		'rp_prefix', 'rp_firstname', 'rp_b_day', 'rp_b_month', 'rp_b_year', 'rp_b_sex', 'rp_b_place', 'rp_b_prov', 
		'rp_b_coh', 'mo_family', 'mo_prefix', 'mo_firstname', 'fa_family', 'fa_prefix', 'fa_firstname' )

class PlaatsAdmin( admin.ModelAdmin ):
	list_display = ( 'id', 'gemnr', 'provnr', 'regnr', 'regio', 'volgnr', 'gemnaam' )


admin.site.register( Hsnrp,  HsnrpAdmin )
admin.site.register( Plaats, PlaatsAdmin )

# [eof]
