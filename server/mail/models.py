# -*- coding: utf-8 -*-

"""
Author:		Fons Laan, KNAW IISH - International Institute of Social History
Project:	HSN Mail
Name:		models.py
Version:	0.3
Goal:		Model classes for the mail tables

* Field names made lowercase by inspectdb (import from legacy MySQL tables). 
* Make sure each model has one field with primary_key = True
* Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table

21-May-2015	Created
09-Sep-2015	Missing table Huwknd added
29-Sep-2015	Added new table ArchiefGemeente
01-Oct-2015	Other new tables
12-Oct-2015	Removed superfloues tables
27-Oct-2015	Changed
"""

# python-future for Python 2/3 compatibility
from __future__ import ( absolute_import, division, print_function, unicode_literals )
from builtins import ( ascii, bytes, chr, dict, filter, hex, input, int, map, next, 
	oct, open, pow, range, round, str, super, zip )

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


class Huwknd( models.Model ):
	id       = models.AutoField(     db_column = 'ID',       primary_key = True )
	idnr     = models.IntegerField(  db_column = 'IDNR',     blank = True, null = True )
	hvlgnr   = models.IntegerField(  db_column = 'HVLGNR',   blank = True, null = True )
	hgemnr   = models.IntegerField(  db_column = 'HGEMNR',   blank = True, null = True )
	haktenr  = models.IntegerField(  db_column = 'HAKTENR',  blank = True, null = True )
	hplts    = models.CharField(     db_column = 'HPLTS',    blank = True, null = True, max_length = 50 )
	huur     = models.IntegerField(  db_column = 'HUUR',     blank = True, null = True )
	hdag     = models.IntegerField(  db_column = 'HDAG',     blank = True, null = True )
	hmaand   = models.IntegerField(  db_column = 'HMAAND',   blank = True, null = True )
	hjaar    = models.IntegerField(  db_column = 'HJAAR',    blank = True, null = True )
	scheidng = models.CharField(     db_column = 'SCHEIDNG', blank = True, null = True, max_length = 1 )
	sdag     = models.IntegerField(  db_column = 'SDAG',     blank = True, null = True )
	smaand   = models.IntegerField(  db_column = 'SMAAND',   blank = True, null = True )
	sjaar    = models.IntegerField(  db_column = 'SJAAR',    blank = True, null = True )
	splts    = models.CharField(     db_column = 'SPLTS',    blank = True, null = True, max_length = 50 )
	idag     = models.IntegerField(  db_column = 'IDAG',     blank = True, null = True )
	imaand   = models.IntegerField(  db_column = 'IMAAND',   blank = True, null = True )
	ijaar    = models.IntegerField(  db_column = 'IJAAR',    blank = True, null = True )
	iplts    = models.CharField(     db_column = 'IPLTS',    blank = True, null = True, max_length = 50 )
	lftjhm   = models.IntegerField(  db_column = 'LFTJHM',   blank = True, null = True )
	lftjhv   = models.IntegerField(  db_column = 'LFTJHV',   blank = True, null = True )
	gebsex   = models.CharField(     db_column = 'GEBSEX',   blank = True, null = True, max_length = 1 )
	anmhm    = models.CharField(     db_column = 'ANMHM',    blank = True, null = True, max_length = 50 )
	tushm    = models.CharField(     db_column = 'TUSHM',    blank = True, null = True, max_length = 10 )
	vrn1hm   = models.CharField(     db_column = 'VRN1HM',   blank = True, null = True, max_length = 20 )
	vrn2hm   = models.CharField(     db_column = 'VRN2HM',   blank = True, null = True, max_length = 20 )
	vrn3hm   = models.CharField(     db_column = 'VRN3HM',   blank = True, null = True, max_length = 30 )
	brphm    = models.CharField(     db_column = 'BRPHM',    blank = True, null = True, max_length = 50 )
	gebplnhm = models.IntegerField(  db_column = 'GEBPLNHM', blank = True, null = True )
	gebplhm  = models.CharField(     db_column = 'GEBPLHM',  blank = True, null = True, max_length = 50 )
	adrhm    = models.CharField(     db_column = 'ADRHM',    blank = True, null = True, max_length = 50 )
	oadrhm   = models.CharField(     db_column = 'OADRHM',   blank = True, null = True, max_length = 50 )
	oadrehm  = models.CharField(     db_column = 'OADREHM',  blank = True, null = True, max_length = 50 )
	bsthm    = models.CharField(     db_column = 'BSTHM',    blank = True, null = True, max_length = 1 )
	hndhm    = models.CharField(     db_column = 'HNDHM',    blank = True, null = True, max_length = 1 )
	anmhv    = models.CharField(     db_column = 'ANMHV',    blank = True, null = True, max_length = 50 )
	tushv    = models.CharField(     db_column = 'TUSHV',    blank = True, null = True, max_length = 10 )
	vrn1hv   = models.CharField(     db_column = 'VRN1HV',   blank = True, null = True, max_length = 20 )
	vrn2hv   = models.CharField(     db_column = 'VRN2HV',   blank = True, null = True, max_length = 20 )
	vrn3hv   = models.CharField(     db_column = 'VRN3HV',   blank = True, null = True, max_length = 30 )
	brphv    = models.CharField(     db_column = 'BRPHV',    blank = True, null = True, max_length = 50 )
	gebplnhv = models.IntegerField(  db_column = 'GEBPLNHV', blank = True, null = True )
	gebplhv  = models.CharField(     db_column = 'GEBPLHV',  blank = True, null = True, max_length = 50 )
	adrhv    = models.CharField(     db_column = 'ADRHV',    blank = True, null = True, max_length = 50 )
	oadrhv   = models.CharField(     db_column = 'OADRHV',   blank = True, null = True, max_length = 50 )
	oadrehv  = models.CharField(     db_column = 'OADREHV',  blank = True, null = True, max_length = 50 )
	bsthv    = models.CharField(     db_column = 'BSTHV',    blank = True, null = True, max_length = 1 )
	hndhv    = models.CharField(     db_column = 'HNDHV',    blank = True, null = True, max_length = 1 )
	levvrhm  = models.CharField(     db_column = 'LEVVRHM',  blank = True, null = True, max_length = 1 )
	toevrhm  = models.CharField(     db_column = 'TOEVRHM',  blank = True, null = True, max_length = 1 )
	anmvrhm  = models.CharField(     db_column = 'ANMVRHM',  blank = True, null = True, max_length = 50 )
	tusvrhm  = models.CharField(     db_column = 'TUSVRHM',  blank = True, null = True, max_length = 10 )
	vrn1vrhm = models.CharField(     db_column = 'VRN1VRHM', blank = True, null = True, max_length = 20 )
	vrn2vrhm = models.CharField(     db_column = 'VRN2VRHM', blank = True, null = True, max_length = 20 )
	vrn3vrhm = models.CharField(     db_column = 'VRN3VRHM', blank = True, null = True, max_length = 30 )
	brpvrhm  = models.CharField(     db_column = 'BRPVRHM',  blank = True, null = True, max_length = 50 )
	adrvrhm  = models.CharField(     db_column = 'ADRVRHM',  blank = True, null = True, max_length = 50 )
	plovvrhm = models.CharField(     db_column = 'PLOVVRHM', blank = True, null = True, max_length = 50 )
	hndvrhm  = models.CharField(     db_column = 'HNDVRHM',  blank = True, null = True, max_length = 1 )
	lftjvrhm = models.IntegerField(  db_column = 'LFTJVRHM', blank = True, null = True )
	levmrhm  = models.CharField(     db_column = 'LEVMRHM',  blank = True, null = True, max_length = 1 )
	toemrhm  = models.CharField(     db_column = 'TOEMRHM',  blank = True, null = True, max_length = 1 )
	anmmrhm  = models.CharField(     db_column = 'ANMMRHM',  blank = True, null = True, max_length = 50 )
	tusmrhm  = models.CharField(     db_column = 'TUSMRHM',  blank = True, null = True, max_length = 10 )
	vrn1mrhm = models.CharField(     db_column = 'VRN1MRHM', blank = True, null = True, max_length = 20 )
	vrn2mrhm = models.CharField(     db_column = 'VRN2MRHM', blank = True, null = True, max_length = 20 )
	vrn3mrhm = models.CharField(     db_column = 'VRN3MRHM', blank = True, null = True, max_length = 30 )
	brpmrhm  = models.CharField(     db_column = 'BRPMRHM',  blank = True, null = True, max_length = 50 )
	adrmrhm  = models.CharField(     db_column = 'ADRMRHM',  blank = True, null = True, max_length = 50 )
	plovmrhm = models.CharField(     db_column = 'PLOVMRHM', blank = True, null = True, max_length = 50 )
	hndmrhm  = models.CharField(     db_column = 'HNDMRHM',  blank = True, null = True, max_length = 1 )
	lftjmrhm = models.IntegerField(  db_column = 'LFTJMRHM', blank = True, null = True )
	levvrhv  = models.CharField(     db_column = 'LEVVRHV',  blank = True, null = True, max_length = 1 )
	toevrhv  = models.CharField(     db_column = 'TOEVRHV',  blank = True, null = True, max_length = 1 )
	anmvrhv  = models.CharField(     db_column = 'ANMVRHV',  blank = True, null = True, max_length = 50 )
	tusvrhv  = models.CharField(     db_column = 'TUSVRHV',  blank = True, null = True, max_length = 10 )
	vrn1vrhv = models.CharField(     db_column = 'VRN1VRHV', blank = True, null = True, max_length = 20 )
	vrn2vrhv = models.CharField(     db_column = 'VRN2VRHV', blank = True, null = True, max_length = 20 )
	vrn3vrhv = models.CharField(     db_column = 'VRN3VRHV', blank = True, null = True, max_length = 30 )
	brpvrhv  = models.CharField(     db_column = 'BRPVRHV',  blank = True, null = True, max_length = 50 )
	adrvrhv  = models.CharField(     db_column = 'ADRVRHV',  blank = True, null = True, max_length = 50 )
	plovvrhv = models.CharField(     db_column = 'PLOVVRHV', blank = True, null = True, max_length = 50 )
	hndvrhv  = models.CharField(     db_column = 'HNDVRHV',  blank = True, null = True, max_length = 1 )
	lftjvrhv = models.IntegerField(  db_column = 'LFTJVRHV', blank = True, null = True )
	levmrhv  = models.CharField(     db_column = 'LEVMRHV',  blank = True, null = True, max_length = 1 )
	toemrhv  = models.CharField(     db_column = 'TOEMRHV',  blank = True, null = True, max_length = 1 )
	anmmrhv  = models.CharField(     db_column = 'ANMMRHV',  blank = True, null = True, max_length = 50 )
	tusmrhv  = models.CharField(     db_column = 'TUSMRHV',  blank = True, null = True, max_length = 10 )
	vrn1mrhv = models.CharField(     db_column = 'VRN1MRHV', blank = True, null = True, max_length = 20 )
	vrn2mrhv = models.CharField(     db_column = 'VRN2MRHV', blank = True, null = True, max_length = 20 )
	vrn3mrhv = models.CharField(     db_column = 'VRN3MRHV', blank = True, null = True, max_length = 30 )
	brpmrhv  = models.CharField(     db_column = 'BRPMRHV',  blank = True, null = True, max_length = 50 )
	adrmrhv  = models.CharField(     db_column = 'ADRMRHV',  blank = True, null = True, max_length = 50 )
	plovmrhv = models.CharField(     db_column = 'PLOVMRHV', blank = True, null = True, max_length = 50 )
	hndmrhv  = models.CharField(     db_column = 'HNDMRHV',  blank = True, null = True, max_length = 1 )
	lftjmrhv = models.IntegerField(  db_column = 'LFTJMRHV', blank = True, null = True )
	ugebhuw  = models.CharField(     db_column = 'UGEBHUW',  blank = True, null = True, max_length = 1 )
	uovloud  = models.CharField(     db_column = 'UOVLOUD',  blank = True, null = True, max_length = 1 )
	uovlech  = models.CharField(     db_column = 'UOVLECH',  blank = True, null = True, max_length = 1 )
	certnatm = models.CharField(     db_column = 'CERTNATM', blank = True, null = True, max_length = 1 )
	toestnot = models.CharField(     db_column = 'TOESTNOT', blank = True, null = True, max_length = 1 )
	aktebek  = models.CharField(     db_column = 'AKTEBEK',  blank = True, null = True, max_length = 1 )
	onvermgn = models.CharField(     db_column = 'ONVERMGN', blank = True, null = True, max_length = 1 )
	command  = models.CharField(     db_column = 'COMMAND',  blank = True, null = True, max_length = 1 )
	toestvgd = models.CharField(     db_column = 'TOESTVGD', blank = True, null = True, max_length = 1 )
	geghuw   = models.CharField(     db_column = 'GEGHUW',   blank = True, null = True, max_length = 1 )
	gegvr    = models.CharField(     db_column = 'GEGVR',    blank = True, null = True, max_length = 1 )
	gegmr    = models.CharField(     db_column = 'GEGMR',    blank = True, null = True, max_length = 1 )
	problm   = models.CharField(     db_column = 'PROBLM',   blank = True, null = True, max_length = 1 )
	ngtg     = models.IntegerField(  db_column = 'NGTG',     blank = True, null = True )
	erken    = models.CharField(     db_column = 'ERKEN',    blank = True, null = True, max_length = 1 )
	arch     = models.CharField(     db_column = 'ARCH',     blank = True, null = True, max_length = 1 )
	opdrnr   = models.CharField(     db_column = 'OPDRNR',   blank = True, null = True, max_length = 3 )
	datum    = models.DateTimeField( db_column = 'DATUM',    blank = True, null = True )
	init     = models.CharField(     db_column = 'INIT',     blank = True, null = True, max_length = 3 )
	versie   = models.CharField(     db_column = 'VERSIE',   blank = True, null = True, max_length = 5 )
	ondrzko  = models.CharField(     db_column = 'ONDRZKO',  blank = True, null = True, max_length = 3 )
	archo    = models.CharField(     db_column = 'ARCHO',    blank = True, null = True, max_length = 1 )
	opdrnro  = models.CharField(     db_column = 'OPDRNRO',  blank = True, null = True, max_length = 3 )
	datumo   = models.DateTimeField( db_column = 'DATUMO',   blank = True, null = True )
	inito    = models.CharField(     db_column = 'INITO',    blank = True, null = True, max_length = 3 )
	versieo  = models.CharField(     db_column = 'VERSIEO',  blank = True, null = True, max_length = 5 )

	class Meta:
		managed  = False
		db_table = 'HUWKND'


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


class Ovlknd( models.Model ):
	id       = models.AutoField(     db_column = 'ID', primary_key = True )
	idnr     = models.IntegerField(  db_column = 'IDNR',     blank = True, null = True )
	oacgemnr = models.IntegerField(  db_column = 'OACGEMNR', blank = True, null = True )
	oacgemnm = models.CharField(     db_column = 'OACGEMNM', blank = True, null = True, max_length = 50 )
	oaktenr  = models.IntegerField(  db_column = 'OAKTENR',  blank = True, null = True )
	oakteuur = models.IntegerField(  db_column = 'OAKTEUUR', blank = True, null = True )
	oaktemin = models.IntegerField(  db_column = 'OAKTEMIN', blank = True, null = True )
	oaktedag = models.IntegerField(  db_column = 'OAKTEDAG', blank = True, null = True )
	oaktemnd = models.IntegerField(  db_column = 'OAKTEMND', blank = True, null = True )
	oaktejr  = models.IntegerField(  db_column = 'OAKTEJR',  blank = True, null = True )
	lengeb   = models.IntegerField(  db_column = 'LENGEB',   blank = True, null = True )
	agvvadr  = models.CharField(     db_column = 'AGVVADR',  blank = True, null = True, max_length = 1 )
	nagvr    = models.IntegerField(  db_column = 'NAGVR',    blank = True, null = True )
	hndtkv   = models.CharField(     db_column = 'HNDTKV',   blank = True, null = True, max_length =  1 )
	gegovl   = models.CharField(     db_column = 'GEGOVL',   blank = True, null = True, max_length =  1 )
	gegvad   = models.CharField(     db_column = 'GEGVAD',   blank = True, null = True, max_length =  1 )
	gegmoe   = models.CharField(     db_column = 'GEGMOE',   blank = True, null = True, max_length =  1 )
	anmovl   = models.CharField(     db_column = 'ANMOVL',   blank = True, null = True, max_length = 50 )
	tusovl   = models.CharField(     db_column = 'TUSOVL',   blank = True, null = True, max_length = 10 )
	vrn1ovl  = models.CharField(     db_column = 'VRN1OVL',  blank = True, null = True, max_length = 20 )
	vrn2ovl  = models.CharField(     db_column = 'VRN2OVL',  blank = True, null = True, max_length = 20 )
	vrn3ovl  = models.CharField(     db_column = 'VRN3OVL',  blank = True, null = True, max_length = 30 )
	laaug    = models.IntegerField(  db_column = 'LAAUG',    blank = True, null = True )
	brpovl   = models.CharField(     db_column = 'BRPOVL',   blank = True, null = True, max_length = 50 )
	gbpovl   = models.IntegerField(  db_column = 'GBPOVL',   blank = True, null = True )
	ggmovl   = models.CharField(     db_column = 'GGMOVL',   blank = True, null = True, max_length = 50 )
	adrovl   = models.CharField(     db_column = 'ADROVL',   blank = True, null = True, max_length = 50 )
	brgovl   = models.CharField(     db_column = 'BRGOVL',   blank = True, null = True, max_length =  1 )
	ovlsex   = models.CharField(     db_column = 'OVLSEX',   blank = True, null = True, max_length =  1 )
	ovldag   = models.IntegerField(  db_column = 'OVLDAG',   blank = True, null = True )
	ovlmnd   = models.IntegerField(  db_column = 'OVLMND',   blank = True, null = True )
	ovljr    = models.IntegerField(  db_column = 'OVLJR',    blank = True, null = True )
	ovluur   = models.IntegerField(  db_column = 'OVLUUR',   blank = True, null = True )
	ovlmin   = models.IntegerField(  db_column = 'OVLMIN',   blank = True, null = True )
	ploovl   = models.CharField(     db_column = 'PLOOVL',   blank = True, null = True, max_length = 50 )
	lftuovl  = models.IntegerField(  db_column = 'LFTUOVL',  blank = True, null = True )
	lftdovl  = models.IntegerField(  db_column = 'LFTDOVL',  blank = True, null = True )
	lftwovl  = models.IntegerField(  db_column = 'LFTWOVL',  blank = True, null = True )
	lftmovl  = models.IntegerField(  db_column = 'LFTMOVL',  blank = True, null = True )
	lftjovl  = models.IntegerField(  db_column = 'LFTJOVL',  blank = True, null = True )
	mreovl   = models.IntegerField(  db_column = 'MREOVL',   blank = True, null = True )
	anmvovl  = models.CharField(     db_column = 'ANMVOVL',  blank = True, null = True, max_length = 50 )
	tusvovl  = models.CharField(     db_column = 'TUSVOVL',  blank = True, null = True, max_length = 10 )
	vrn1vovl = models.CharField(     db_column = 'VRN1VOVL', blank = True, null = True, max_length = 20 )
	vrn2vovl = models.CharField(     db_column = 'VRN2VOVL', blank = True, null = True, max_length = 20 )
	vrn3vovl = models.CharField(     db_column = 'VRN3VOVL', blank = True, null = True, max_length = 30 )
	levvovl  = models.CharField(     db_column = 'LEVVOVL',  blank = True, null = True, max_length =  1 )
	brpvovl  = models.CharField(     db_column = 'BRPVOVL',  blank = True, null = True, max_length = 50 )
	lfvrovl  = models.IntegerField(  db_column = 'LFVROVL',  blank = True, null = True )
	adrvovl  = models.CharField(     db_column = 'ADRVOVL',  blank = True, null = True, max_length = 50 )
	anmmovl  = models.CharField(     db_column = 'ANMMOVL',  blank = True, null = True, max_length = 50 )
	tusmovl  = models.CharField(     db_column = 'TUSMOVL',  blank = True, null = True, max_length = 10 )
	vrn1movl = models.CharField(     db_column = 'VRN1MOVL', blank = True, null = True, max_length = 20 )
	vrn2movl = models.CharField(     db_column = 'VRN2MOVL', blank = True, null = True, max_length = 20 )
	vrn3movl = models.CharField(     db_column = 'VRN3MOVL', blank = True, null = True, max_length = 30 )
	levmovl  = models.CharField(     db_column = 'LEVMOVL',  blank = True, null = True, max_length =  1 )
	brpmovl  = models.CharField(     db_column = 'BRPMOVL',  blank = True, null = True, max_length = 50 )
	lfmrovl  = models.IntegerField(  db_column = 'LFMROVL',  blank = True, null = True )
	adrmovl  = models.CharField(     db_column = 'ADRMOVL',  blank = True, null = True, max_length = 50 )
	extract  = models.CharField(     db_column = 'EXTRACT',  blank = True, null = True, max_length =  1 )
	problm   = models.CharField(     db_column = 'PROBLM',   blank = True, null = True, max_length =  1 )
	arch     = models.CharField(     db_column = 'ARCH',     blank = True, null = True, max_length =  1 )
	opdrnr   = models.CharField(     db_column = 'OPDRNR',   blank = True, null = True, max_length =  3 )
	datum    = models.DateTimeField( db_column = 'DATUM',    blank = True, null = True )
	init     = models.CharField(     db_column = 'INIT',     blank = True, null = True, max_length = 3 )
	versie   = models.CharField(     db_column = 'VERSIE',   blank = True, null = True, max_length = 5 )
	ondrzko  = models.CharField(     db_column = 'ONDRZKO',  blank = True, null = True, max_length = 3 )
	archo    = models.CharField(     db_column = 'ARCHO',    blank = True, null = True, max_length = 1 )
	opdrnro  = models.CharField(     db_column = 'OPDRNRO',  blank = True, null = True, max_length = 3 )
	datumo   = models.DateTimeField( db_column = 'DATUMO',   blank = True, null = True )
	inito    = models.CharField(     db_column = 'INITO',    blank = True, null = True, max_length = 3 )
	versieo  = models.CharField(     db_column = 'VERSIEO',  blank = True, null = True, max_length = 5 )

	class Meta:
		managed  = False
		db_table = 'OVLKND'


class Pkknd(models.Model):
	id        = models.AutoField(     db_column = 'ID', primary_key = True )
	idnr      = models.IntegerField(  db_column = 'IDNR',      blank = True, null = True )
	idnrp     = models.IntegerField(  db_column = 'IDNRP',     blank = True, null = True )
	gaktnrp   = models.CharField(     db_column = 'GAKTNRP',   blank = True, null = True, max_length = 8 )
	pktype    = models.IntegerField(  db_column = 'PKTYPE',    blank = True, null = True )
	eindagpk  = models.IntegerField(  db_column = 'EINDAGPK',  blank = True, null = True )
	einmndpk  = models.IntegerField(  db_column = 'EINMNDPK',  blank = True, null = True )
	einjarpk  = models.IntegerField(  db_column = 'EINJARPK',  blank = True, null = True )
	ctrdgp    = models.IntegerField(  db_column = 'CTRDGP',    blank = True, null = True )
	ctrmdp    = models.IntegerField(  db_column = 'CTRMDP',    blank = True, null = True )
	ctrjrp    = models.IntegerField(  db_column = 'CTRJRP',    blank = True, null = True )
	ctrparp   = models.CharField(     db_column = 'CTRPARP',   blank = True, null = True, max_length = 1 )
	gznvrmp   = models.CharField(     db_column = 'GZNVRMP',   blank = True, null = True, max_length = 50 )
	anmperp   = models.CharField(     db_column = 'ANMPERP',   blank = True, null = True, max_length = 50 )
	tusperp   = models.CharField(     db_column = 'TUSPERP',   blank = True, null = True, max_length = 10 )
	vnm1perp  = models.CharField(     db_column = 'VNM1PERP',  blank = True, null = True, max_length = 20 )
	vnm2perp  = models.CharField(     db_column = 'VNM2PERP',  blank = True, null = True, max_length = 20 )
	vnm3perp  = models.CharField(     db_column = 'VNM3PERP',  blank = True, null = True, max_length = 30 )
	gdgperp   = models.IntegerField(  db_column = 'GDGPERP',   blank = True, null = True )
	gmdperp   = models.IntegerField(  db_column = 'GMDPERP',   blank = True, null = True )
	gjrperp   = models.IntegerField(  db_column = 'GJRPERP',   blank = True, null = True )
	gdgperpcr = models.IntegerField(  db_column = 'GDGPERPCR', blank = True, null = True )
	gmdperpcr = models.IntegerField(  db_column = 'GMDPERPCR', blank = True, null = True )
	gjrperpcr = models.IntegerField(  db_column = 'GJRPERPCR', blank = True, null = True )
	gplperp   = models.CharField(     db_column = 'GPLPERP',   blank = True, null = True, max_length = 50 )
	natperp   = models.CharField(     db_column = 'NATPERP',   blank = True, null = True, max_length = 40 )
	gdsperp   = models.CharField(     db_column = 'GDSPERP',   blank = True, null = True, max_length = 20 )
	gslperp   = models.CharField(     db_column = 'GSLPERP',   blank = True, null = True, max_length = 1 )
	anmvdrp   = models.CharField(     db_column = 'ANMVDRP',   blank = True, null = True, max_length = 50 )
	tusvdrp   = models.CharField(     db_column = 'TUSVDRP',   blank = True, null = True, max_length = 10 )
	vnm1vdrp  = models.CharField(     db_column = 'VNM1VDRP',  blank = True, null = True, max_length = 20 )
	vnm2vdrp  = models.CharField(     db_column = 'VNM2VDRP',  blank = True, null = True, max_length = 20 )
	vnm3vdrp  = models.CharField(     db_column = 'VNM3VDRP',  blank = True, null = True, max_length = 30 )
	gdgvdrp   = models.IntegerField(  db_column = 'GDGVDRP',   blank = True, null = True )
	gmdvdrp   = models.IntegerField(  db_column = 'GMDVDRP',   blank = True, null = True )
	gjrvdrp   = models.IntegerField(  db_column = 'GJRVDRP',   blank = True, null = True )
	gdgvdrpcr = models.IntegerField(  db_column = 'GDGVDRPCR', blank = True, null = True )
	gmdvdrpcr = models.IntegerField(  db_column = 'GMDVDRPCR', blank = True, null = True )
	gjrvdrpcr = models.IntegerField(  db_column = 'GJRVDRPCR', blank = True, null = True )
	gplvdrp   = models.CharField(     db_column = 'GPLVDRP',   blank = True, null = True, max_length = 50 )
	anmmdrp   = models.CharField(     db_column = 'ANMMDRP',   blank = True, null = True, max_length = 50 )
	tusmdrp   = models.CharField(     db_column = 'TUSMDRP',   blank = True, null = True, max_length = 10 )
	vnm1mdrp  = models.CharField(     db_column = 'VNM1MDRP',  blank = True, null = True, max_length = 20 )
	vnm2mdrp  = models.CharField(     db_column = 'VNM2MDRP',  blank = True, null = True, max_length = 20 )
	vnm3mdrp  = models.CharField(     db_column = 'VNM3MDRP',  blank = True, null = True, max_length = 30 )
	gdgmdrp   = models.IntegerField(  db_column = 'GDGMDRP',   blank = True, null = True )
	gmdmdrp   = models.IntegerField(  db_column = 'GMDMDRP',   blank = True, null = True )
	gjrmdrp   = models.IntegerField(  db_column = 'GJRMDRP',   blank = True, null = True )
	gdgmdrpcr = models.IntegerField(  db_column = 'GDGMDRPCR', blank = True, null = True )
	gmdmdrpcr = models.IntegerField(  db_column = 'GMDMDRPCR', blank = True, null = True )
	gjrmdrpcr = models.IntegerField(  db_column = 'GJRMDRPCR', blank = True, null = True )
	gplmdrp   = models.CharField(     db_column = 'GPLMDRP',   blank = True, null = True, max_length = 50 )
	odgperp   = models.IntegerField(  db_column = 'ODGPERP',   blank = True, null = True )
	omdperp   = models.IntegerField(  db_column = 'OMDPERP',   blank = True, null = True )
	ojrperp   = models.IntegerField(  db_column = 'OJRPERP',   blank = True, null = True )
	oplperp   = models.CharField(     db_column = 'OPLPERP',   blank = True, null = True, max_length = 50 )
	oakperp   = models.CharField(     db_column = 'OAKPERP',   blank = True, null = True, max_length = 10 )
	odoperp   = models.CharField(     db_column = 'ODOPERP',   blank = True, null = True, max_length = 50 )
	gegperp   = models.CharField(     db_column = 'GEGPERP',   blank = True, null = True, max_length = 1 )
	gegvdrp   = models.CharField(     db_column = 'GEGVDRP',   blank = True, null = True, max_length = 1 )
	gegmdrp   = models.CharField(     db_column = 'GEGMDRP',   blank = True, null = True, max_length = 1 )
	problmp   = models.CharField(     db_column = 'PROBLMP',   blank = True, null = True, max_length = 1 )
	psbdgp    = models.IntegerField(  db_column = 'PSBDGP',    blank = True, null = True )
	psbmdp    = models.IntegerField(  db_column = 'PSBMDP',    blank = True, null = True )
	psbjrp    = models.IntegerField(  db_column = 'PSBJRP',    blank = True, null = True )
	psbnrp    = models.CharField(     db_column = 'PSBNRP',    blank = True, null = True, max_length = 10 )
	opdrnr    = models.CharField(     db_column = 'OPDRNR',    blank = True, null = True, max_length = 3 )
	datum     = models.DateTimeField( db_column = 'DATUM',     blank = True, null = True )
	init      = models.CharField(     db_column = 'INIT',      blank = True, null = True, max_length = 3 )
	versie    = models.CharField(     db_column = 'VERSIE',    blank = True, null = True, max_length = 5 )
	ondrzko   = models.CharField(     db_column = 'ONDRZKO',   blank = True, null = True, max_length = 3 )
	opdrnro   = models.CharField(     db_column = 'OPDRNRO',   blank = True, null = True, max_length = 3 )
	datumo    = models.DateTimeField( db_column = 'DATUMO',    blank = True, null = True )
	inito     = models.CharField(     db_column = 'INITO',     blank = True, null = True, max_length = 3 )
	versieo   = models.CharField(     db_column = 'VERSIEO',   blank = True, null = True, max_length = 5 )

	class Meta:
		managed  = False
		db_table = 'PKKND'


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
		db_table = 'PLAATS'
		unique_together = (('gemnr', 'volgnr'),)


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
