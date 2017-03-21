# -*- coding: utf-8 -*-

"""
Author:		Fons Laan, KNAW IISH - International Institute of Social History
Project:	HSN Mail
Name:		models.py
Version:	1.0.1
Goal:		Model classes for the hsn_reference tables

08-Mar-2016	Created
20-Mar-2017	Changed
"""

# future-0.16.0 imports for Python 2/3 compatibility
from __future__ import ( absolute_import, division, print_function, unicode_literals )
from builtins import ( ascii, bytes, chr, dict, filter, hex, input, int, list, map, 
    next, object, oct, open, pow, range, round, super, str, zip )

from django.db import models


class Hsnrp(models.Model):
	id           = models.AutoField(    db_column = 'Id',           primary_key = True )
	idnr         = models.IntegerField( db_column = 'IDNR',         blank = True, null = True )
	id_origin    = models.IntegerField( db_column = 'ID_origin',    blank = True, null = True )
	project      = models.CharField(    db_column = 'Project',      blank = True, null = True, max_length = 255 )
	gemnr        = models.IntegerField( db_column = 'Gemnr',        blank = True, null = True )
	valid_day    = models.IntegerField( db_column = 'Valid_day',    blank = True, null = True )
	valid_month  = models.IntegerField( db_column = 'Valid_month',  blank = True, null = True )
	valid_year   = models.IntegerField( db_column = 'Valid_year',   blank = True, null = True )
	rp_family    = models.CharField(    db_column = 'RP_family',    blank = True, null = True, max_length = 60 )
	rp_prefix    = models.CharField(    db_column = 'RP_prefix',    blank = True, null = True, max_length = 255 )
	rp_firstname = models.CharField(    db_column = 'RP_firstname', blank = True, null = True, max_length = 255,  )
	rp_b_day     = models.IntegerField( db_column = 'RP_B_DAY',     blank = True, null = True )
	rp_b_month   = models.IntegerField( db_column = 'RP_B_MONTH',   blank = True, null = True )
	rp_b_year    = models.IntegerField( db_column = 'RP_B_YEAR',    blank = True, null = True )
	rp_b_sex     = models.CharField(    db_column = 'RP_B_SEX',     blank = True, null = True, max_length = 1 )
	rp_b_place   = models.CharField(    db_column = 'RP_B_PLACE',   blank = True, null = True, max_length = 50 )
	rp_b_prov    = models.IntegerField( db_column = 'RP_B_PROV',    blank = True, null = True )
	rp_b_coh     = models.IntegerField( db_column = 'RP_B_COH',     blank = True, null = True )
	mo_family    = models.CharField(    db_column = 'MO_family',    blank = True, null = True, max_length = 60 )
	mo_prefix    = models.CharField(    db_column = 'MO_prefix',    blank = True, null = True, max_length = 255,  )
	mo_firstname = models.CharField(    db_column = 'MO_firstname', blank = True, null = True, max_length = 255 )
	fa_family    = models.CharField(    db_column = 'FA_family',    blank = True, null = True, max_length = 60 )
	fa_prefix    = models.CharField(    db_column = 'FA_prefix',    blank = True, null = True, max_length = 255 )
	fa_firstname = models.CharField(    db_column = 'FA_firstname', blank = True, null = True, max_length = 255 )

	class Meta:
		managed  = False
		db_table = 'HSNRP'


class Plaats( models.Model ):
	id      = models.AutoField(    db_column = 'ID', primary_key = True )
	gemnr   = models.IntegerField( db_column = 'GEMNR')
	provnr  = models.IntegerField( db_column = 'PROVNR', blank = True, null = True )
	regnr   = models.IntegerField( db_column = 'REGNR',  blank = True, null = True )
	regio   = models.CharField(    db_column = 'REGIO',  blank = True, null = True, max_length = 20 )
	volgnr  = models.IntegerField( db_column = 'VOLGNR' )
	gemnaam = models.CharField(    db_column = 'GEMNAAM', blank = True, null = True, max_length = 50 )

	class Meta:
		managed = False
		db_table = 'ref_plaats'
		unique_together = (('gemnr', 'volgnr'),)

# [eof]
