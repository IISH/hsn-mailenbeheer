# -*- coding: utf-8 -*-

"""
Author:		Fons Laan, KNAW IISH - International Institute of Social History
Project:	HSN Mail
Name:		admin.py
Version:	1.0.0
Goal:		Admin classes for the hsn_central tables

08-Mar-2016	Created
17-Mar-2016	Changed
"""


from django.contrib import admin

from .models import ( Huwknd, Ovlknd, Pkknd )


class HuwkndAdmin( admin.ModelAdmin ):
	list_display = ( 'id', 'idnr', 'hvlgnr', 'hgemnr', 'haktenr', 'hplts', 'huur', 'hdag', 'hmaand', 'hjaar',
		'scheidng', 'sdag', 'smaand', 'sjaar', 'splts', 'idag', 'imaand', 'ijaar', 'iplts', 'lftjhm', 'lftjhv', 
		'gebsex', 'anmhm', 'tushm', 'vrn1hm', 'vrn2hm', 'vrn3hm', 'brphm', 'gebplnhm', 'gebplhm', 'adrhm', 
		'oadrhm', 'oadrehm', 'bsthm', 'hndhm', 'anmhv', 'tushv', 'vrn1hv', 'vrn2hv', 'vrn3hv', 'brphv', 'gebplnhv', 
		'gebplhv', 'adrhv', 'oadrhv', 'oadrehv', 'bsthv', 'hndhv', 'levvrhm', 'toevrhm', 'anmvrhm', 'tusvrhm', 
		'vrn1vrhm', 'vrn2vrhm', 'vrn3vrhm', 'brpvrhm', 'adrvrhm', 'plovvrhm', 'hndvrhm', 'lftjvrhm', 'levmrhm', 
		'toemrhm', 'anmmrhm', 'tusmrhm', 'vrn1mrhm', 'vrn2mrhm', 'vrn3mrhm', 'brpmrhm', 'adrmrhm', 'plovmrhm', 
		'hndmrhm', 'lftjmrhm', 'levvrhv', 'toevrhv', 'anmvrhv', 'tusvrhv', 'vrn1vrhv', 'vrn2vrhv', 'vrn3vrhv', 
		'brpvrhv', 'adrvrhv', 'plovvrhv', 'hndvrhv', 'lftjvrhv', 'levmrhv', 'toemrhv', 'anmmrhv', 'tusmrhv', 
		'vrn1mrhv', 'vrn2mrhv', 'vrn3mrhv', 'brpmrhv', 'adrmrhv', 'plovmrhv', 'hndmrhv', 'lftjmrhv', 'ugebhuw', 
		'uovloud', 'uovlech', 'certnatm', 'toestnot', 'aktebek', 'onvermgn', 'command', 'toestvgd', 'geghuw', 
		'gegvr', 'gegmr', 'problm', 'ngtg', 'erken', 'arch', 'opdrnr', 'datum', 'init', 'versie', 'ondrzko', 
		'archo', 'opdrnro', 'datumo', 'inito', 'versieo' )

class OvlkndAdmin( admin.ModelAdmin ):
    list_display = ( 'id', 'idnr', 'oacgemnr', 'oacgemnm', 'oaktenr', 'oakteuur', 'oaktemin', 'oaktedag', 
		'oaktemnd', 'oaktejr', 'lengeb', 'agvvadr', 'nagvr', 'hndtkv', 'gegovl', 'gegvad', 'gegmoe', 'anmovl', 
		'tusovl', 'vrn1ovl', 'vrn2ovl', 'vrn3ovl', 'laaug', 'brpovl', 'gbpovl', 'ggmovl', 'adrovl', 'brgovl', 
		'ovlsex', 'ovldag', 'ovlmnd', 'ovljr', 'ovluur', 'ovlmin', 'ploovl', 'lftuovl', 'lftdovl', 'lftwovl', 
		'lftmovl', 'lftjovl', 'mreovl', 'anmvovl', 'tusvovl', 'vrn1vovl', 'vrn2vovl', 'vrn3vovl', 'levvovl', 
		'brpvovl', 'lfvrovl', 'adrvovl', 'anmmovl', 'tusmovl', 'vrn1movl', 'vrn2movl', 'vrn3movl', 'levmovl', 
		'brpmovl', 'lfmrovl', 'adrmovl', 'extract', 'problm', 'arch', 'opdrnr', 'datum', 'init', 'versie', 
		'ondrzko', 'archo', 'opdrnro', 'datumo', 'inito', 'versieo' )

class PkkndAdmin( admin.ModelAdmin ):
	list_display = ( 'id', 'idnr', 'idnrp', 'gaktnrp', 'pktype', 'eindagpk', 'einmndpk', 'einjarpk', 'ctrdgp', 
		'ctrmdp', 'ctrjrp', 'ctrparp', 'gznvrmp', 'anmperp', 'tusperp', 'vnm1perp', 'vnm2perp', 'vnm3perp', 
		'gdgperp', 'gmdperp', 'gjrperp', 'gdgperpcr', 'gmdperpcr', 'gjrperpcr', 'gplperp', 'natperp', 'gdsperp', 
		'gslperp', 'anmvdrp', 'tusvdrp', 'vnm1vdrp', 'vnm2vdrp', 'vnm3vdrp', 'gdgvdrp', 'gmdvdrp', 'gjrvdrp', 
		'gdgvdrpcr', 'gmdvdrpcr', 'gjrvdrpcr', 'gplvdrp', 'anmmdrp', 'tusmdrp', 'vnm1mdrp', 'vnm2mdrp', 'vnm3mdrp', 
		'gdgmdrp', 'gmdmdrp', 'gjrmdrp', 'gdgmdrpcr', 'gmdmdrpcr', 'gjrmdrpcr', 'gplmdrp', 'odgperp', 'omdperp', 
		'ojrperp', 'oplperp', 'oakperp', 'odoperp', 'gegperp', 'gegvdrp', 'gegmdrp', 'problmp', 'psbdgp', 'psbmdp', 
		'psbjrp', 'psbnrp', 'opdrnr', 'datum', 'init', 'versie', 'ondrzko', 'opdrnro', 'datumo', 'inito', 'versieo' )


"""
# We have to adapt the admin classes above for multi-db support, see: 
# https://docs.djangoproject.com/en/1.9/topics/db/multi-db/
admin.site.register( Huwknd, HuwkndAdmin )
admin.site.register( Ovlknd, OvlkndAdmin )
admin.site.register( Pkknd,  PkkndAdmin )
"""

# [eof]
