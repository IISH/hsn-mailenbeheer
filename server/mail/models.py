# -*- coding: utf-8 -*-

"""
Author:		Fons Laan, KNAW IISH - International Institute of Social History
Project:	HSN Mail
Name:		models.py
Version:	1.0.1
Goal:		Model classes for the hsn_mail tables

* Field names made lowercase by inspectdb (import from legacy MySQL tables). 
* Make sure each model has one field with primary_key = True
* Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table

21-May-2015	Created
09-Sep-2015	Missing table Huwknd added
29-Sep-2015	Added new table ArchiefGemeente
01-Oct-2015	Other new tables
12-Oct-2015	Removed superfloues tables
08-Mar-2016	Split off hsn_central and hsn_reference tables
20-Mar-2017	Changed
"""

# future-0.16.0 imports for Python 2/3 compatibility
from __future__ import ( absolute_import, division, print_function, unicode_literals )
from builtins import ( ascii, bytes, chr, dict, filter, hex, input, int, list, map, 
    next, object, oct, open, pow, range, round, super, str, zip )

from django.db import models


class ArchiefGemeente( models.Model ):
	id                   = models.AutoField(    db_column = 'ID',                   primary_key = True )
	gemnr                = models.IntegerField( db_column = 'Gemnr',                blank = True, null = True )
	provnr               = models.IntegerField( db_column = 'Provnr',               blank = True, null = True )
	gemnaam              = models.CharField(    db_column = 'Gemnaam',              blank = True, null = True, max_length =  50 )
	archiefnaam          = models.CharField(    db_column = 'Archiefnaam',          blank = True, null = True, max_length = 254 )
	gemeente_met_archief = models.CharField(    db_column = 'Gemeente_met_archief', blank = True, null = True, max_length = 255 )
	bezoekadres          = models.CharField(    db_column = 'Bezoekadres',          blank = True, null = True, max_length = 254 )
	postadres            = models.CharField(    db_column = 'Postadres',            blank = True, null = True, max_length = 254 )
	postcode             = models.CharField(    db_column = 'Postcode',             blank = True, null = True, max_length = 254 )
	plaats               = models.CharField(    db_column = 'Plaats',               blank = True, null = True, max_length = 254 )

	class Meta:
		managed  = False
		db_table = 'Archief_gemeente'


class HsnBeheer( models.Model ):
	idnr          = models.AutoField(    db_column = 'Idnr',          primary_key = True )
	ovldag        = models.IntegerField( db_column = 'Ovldag',        blank = True, null = True )
	ovlmnd        = models.IntegerField( db_column = 'Ovlmnd',        blank = True, null = True )
	ovljaar       = models.IntegerField( db_column = 'Ovljaar',       blank = True, null = True )
	fase_a        = models.IntegerField( db_column = 'Fase_A',        blank = True, null = True )
	fase_b        = models.IntegerField( db_column = 'Fase_B',        blank = True, null = True )
	fase_c_d      = models.IntegerField( db_column = 'Fase_C_D',      blank = True, null = True )
	ovlplaats     = models.CharField(    db_column = 'OvlPlaats',     blank = True, null = True, max_length = 50 )
	mail_type     = models.CharField(    db_column = 'Mail_type',     blank = True, null = True, max_length =  1 )
	invoerstatus  = models.CharField(    db_column = 'Invoerstatus',  blank = True, null = True, max_length =  1 )
	randomgetal   = models.IntegerField( db_column = 'Randomgetal',   blank = True, null = True )
	releasestatus = models.CharField(    db_column = 'Releasestatus', blank = True, null = True, max_length =  1 )

	class Meta:
		managed  = False
		db_table = 'HSN_BEHEER'


class HsnIdmut( models.Model ):
	id           = models.AutoField(    db_column = 'Id',           primary_key = True )
	idnr         = models.IntegerField( db_column = 'IDNR',         blank = True, null = True )
	id_origin    = models.IntegerField( db_column = 'ID_Origin',    blank = True, null = True )
	source       = models.CharField(    db_column = 'Source',       blank = True, null = True, max_length = 100 )
	valid_day    = models.IntegerField( db_column = 'Valid_day',    blank = True, null = True )
	valid_month  = models.IntegerField( db_column = 'Valid_month',  blank = True, null = True )
	valid_year   = models.IntegerField( db_column = 'Valid_year',   blank = True, null = True )
	rp_family    = models.CharField(    db_column = 'RP_family',    blank = True, null = True, max_length = 50 )
	rp_prefix    = models.CharField(    db_column = 'RP_prefix',    blank = True, null = True, max_length = 255 )
	rp_firstname = models.CharField(    db_column = 'RP_firstname', blank = True, null = True, max_length = 50 )
	rp_b_day     = models.IntegerField( db_column = 'RP_B_DAY',     blank = True, null = True )
	rp_b_month   = models.IntegerField( db_column = 'RP_B_MONTH',   blank = True, null = True )
	rp_b_year    = models.IntegerField( db_column = 'RP_B_YEAR',    blank = True, null = True )
	rp_b_place   = models.CharField(    db_column = 'RP_B_PLACE',   blank = True, null = True, max_length = 30 )
	rp_b_sex     = models.CharField(    db_column = 'RP_B_SEX',     blank = True, null = True, max_length = 1 )
	remarks      = models.CharField(    db_column = 'Remarks',      blank = True, null = True, max_length = 100 )

	class Meta:
		managed  = False
		db_table = 'HSN_IDMUT'


class HsnKwyt( models.Model ):
	id         = models.AutoField(    db_column = 'ID',         primary_key = True )
	idnr       = models.IntegerField( db_column = 'Idnr',       blank = True, null = True )
	idvolgnr   = models.IntegerField( db_column = 'Idvolgnr',   blank = True, null = True )
	startdag   = models.IntegerField( db_column = 'Startdag',   blank = True, null = True )
	startmaand = models.IntegerField( db_column = 'Startmaand', blank = True, null = True )
	startjaar  = models.IntegerField( db_column = 'Startjaar',  blank = True, null = True )
	eindedag   = models.IntegerField( db_column = 'Eindedag',   blank = True, null = True )
	eindemaand = models.IntegerField( db_column = 'Eindemaand', blank = True, null = True )
	eindejaar  = models.IntegerField( db_column = 'Eindejaar',  blank = True, null = True )
	gevonden   = models.CharField(    blank = True, null = True, max_length = 1 )
	reden      = models.IntegerField( blank = True, null = True )
	locatie    = models.CharField(    blank = True, null = True, max_length = 50 )

	class Meta:
		managed  = False
		db_table = 'HSN_KWYT'


class Mail( models.Model ):
	id          = models.AutoField(    db_column = 'ID', primary_key = True )
	idnr        = models.IntegerField( db_column = 'Idnr',        blank = True, null = True )
	briefnr     = models.IntegerField( db_column = 'Briefnr',     blank = True, null = True )
	aard        = models.CharField(    db_column = 'Aard',        blank = True, null = True, max_length =  1 )
	datum       = models.CharField(    db_column = 'Datum',       blank = True, null = True, max_length = 12 )
	periode     = models.CharField(    db_column = 'Periode',     blank = True, null = True, max_length = 20 )
	gemnr       = models.IntegerField( db_column = 'Gemnr',       blank = True, null = True )
	naamgem     = models.CharField(    db_column = 'Naamgem',     blank = True, null = True, max_length = 50 )
	status      = models.IntegerField( db_column = 'Status',      blank = True, null = True )
	printdatum  = models.CharField(    db_column = 'Printdatum',  blank = True, null = True, max_length = 15 )
	printen     = models.IntegerField( db_column = 'Printen',     blank = True, null = True )
	ontvdat     = models.CharField(    db_column = 'Ontvdat',     blank = True, null = True, max_length = 15 )
	opmerk      = models.TextField(    db_column = 'Opmerk',      blank = True, null = True )
	opident     = models.CharField(    db_column = 'Opident',     blank = True, null = True, max_length = 150 )
	oppartner   = models.CharField(    db_column = 'Oppartner',   blank = True, null = True, max_length = 150 )
	opvader     = models.CharField(    db_column = 'OpVader',     blank = True, null = True, max_length = 100 )
	opmoeder    = models.CharField(    db_column = 'Opmoeder',    blank = True, null = True, max_length = 100 )
	type        = models.CharField(    db_column = 'Type',        blank = True, null = True, max_length =  50 )
	infoouders  = models.IntegerField( db_column = 'InfoOuders',  blank = True, null = True )
	infopartner = models.IntegerField( db_column = 'InfoPartner', blank = True, null = True )
	inforeis    = models.IntegerField( db_column = 'InfoReis',    blank = True, null = True )

	class Meta:
		managed  = False
		db_table = 'MAIL'


class TekstFaseA( models.Model ):
	id          = models.AutoField(    db_column = 'ID', primary_key = True )
	fase_a      = models.IntegerField( db_column = 'fase_A', blank = True, null = True )
	fase_a_text = models.CharField(    db_column = 'fase_A text', max_length = 50, blank = True, null = True )

	class Meta:
		managed  = False
		db_table = 'Tekst_faseA'


class TekstFaseB( models.Model ):
	id          = models.AutoField(    db_column = 'ID', primary_key = True )
	fase_b      = models.IntegerField( db_column = 'fase_B', blank = True, null = True )
	fase_b_text = models.CharField(    db_column = 'fase_B text', max_length = 50, blank = True, null = True )

	class Meta:
		managed  = False
		db_table = 'Tekst_faseB'


class TekstFaseCD( models.Model ):
	id            = models.AutoField(    db_column = 'ID', primary_key = True )
	fase_c_d      = models.IntegerField( db_column = 'fase_C_D', blank = True, null = True )
	fase_c_d_text = models.CharField(    db_column = 'fase_C_D text', max_length = 50, blank = True, null = True )

	class Meta:
		managed  = False
		db_table = 'Tekst_faseC_D'


class TekstGevonden( models.Model ):
	id            = models.AutoField( db_column = 'ID', primary_key = True )
	gevonden      = models.CharField( max_length = 50, blank = True, null = True )
	text_gevonden = models.CharField( db_column = 'text-gevonden', max_length = 50, blank = True, null = True )

	class Meta:
		managed  = False
		db_table = 'Tekst_gevonden'


class TekstReden( models.Model ):
	id         = models.AutoField( db_column = 'ID', primary_key = True )
	reden      = models.IntegerField( blank = True, null = True )
	reden_text = models.CharField( max_length = 50, blank = True, null = True )

	class Meta:
		managed  = False
		db_table = 'Tekst_reden'


class TekstVoortgang( models.Model ):
	id                = models.AutoField( db_column = 'Id', primary_key = True )
	invoerstatus      = models.CharField( db_column = 'Invoerstatus', max_length = 1, blank = True, null = True )
	invoerstatustekst = models.CharField( db_column = 'Invoerstatustekst', max_length = 100, blank = True, null = True )

	class Meta:
		managed  = False
		db_table = 'Tekst_voortgang'

# [eof]
