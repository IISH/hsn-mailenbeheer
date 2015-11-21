# -*- coding: utf-8 -*-

"""
Author:		Fons Laan, KNAW IISH - International Institute of Social History
Project:	HSN Mail
Name:		admin.py
Version:	1.0.0
Goal:		Admin classes for the mail tables

26-May-2015	Created
09-Sep-2015	Missing HuwkndAdmin added
12-Oct-2015	Removed superfluous tables
27-Oct-2015	Changed
"""


from django.contrib import admin

from .models import ( ArchiefGemeente, HsnBeheer, HsnIdmut, HsnKwyt, Hsnrp, Huwknd, Mail, Ovlknd, Pkknd, Plaats )

from .models import ( TekstFaseA, TekstFaseB, TekstFaseCD, TekstGevonden, TekstReden, TekstVoortgang )


# Amin classes for list display
class ArchiefGemeenteAdmin( admin.ModelAdmin ):
	list_display = ( 'id', 'gemnr', 'provnr', 'gemnaam', 'archiefnaam', 'gemeente_met_archief',  'bezoekadres', 'postadres', 
		'postcode',  'plaats' )

class HsnBeheerAdmin( admin.ModelAdmin ):
	list_display = ( 'idnr', 'ovldag', 'ovlmnd', 'ovljaar', 'fase_a', 'fase_b', 'fase_c_d', 'ovlplaats', 
		'mail_type', 'invoerstatus', 'randomgetal', 'releasestatus' )

class HsnIdmutAdmin( admin.ModelAdmin ):
	list_display = ( 'id', 'idnr', 'id_origin', 'source', 'valid_day', 'valid_month', 'valid_year', 'rp_family', 'rp_prefix', 
		'rp_firstname', 'rp_b_day', 'rp_b_month', 'rp_b_year', 'rp_b_place', 'rp_b_sex', 'remarks' )

class HsnKwytAdmin( admin.ModelAdmin ):
	list_display = ( 'id', 'idnr', 'idvolgnr', 'startdag', 'startmaand', 'startjaar', 'eindedag', 'eindemaand', 
		'eindejaar', 'gevonden', 'reden', 'locatie' )

class HsnrpAdmin( admin.ModelAdmin ):
	list_display = ( 'id', 'idnr', 'id_origin', 'project', 'gemnr', 'valid_day', 'valid_month', 'valid_year', 'rp_family', 
		'rp_prefix', 'rp_firstname', 'rp_b_day', 'rp_b_month', 'rp_b_year', 'rp_b_sex', 'rp_b_place', 'rp_b_prov', 
		'rp_b_coh', 'mo_family', 'mo_prefix', 'mo_firstname', 'fa_family', 'fa_prefix', 'fa_firstname' )

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

class MailAdmin( admin.ModelAdmin ):
    list_display = ( 'id', 'idnr', 'briefnr', 'aard', 'datum', 'periode', 'gemnr', 'naamgem', 'status', 
		'printdatum', 'printen', 'ontvdat', 'opmerk', 'opident', 'oppartner', 'opvader', 'opmoeder', 'type', 
		'infoouders', 'infopartner', 'inforeis' )

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

class PlaatsAdmin( admin.ModelAdmin ):
	list_display = ( 'id', 'gemnr', 'provnr', 'regnr', 'regio', 'volgnr', 'gemnaam' )


class TekstFaseAAdmin( admin.ModelAdmin ):
	list_display = ( 'id', 'fase_a', 'fase_a_text' )

class TekstFaseBAdmin( admin.ModelAdmin ):
	list_display = ( 'id', 'fase_b', 'fase_b_text' )

class TekstFaseCDAdmin( admin.ModelAdmin ):
	list_display = ( 'id', 'fase_c_d', 'fase_c_d_text' )

class TekstGevondenAdmin( admin.ModelAdmin ):
	list_display = ( 'id', 'gevonden', 'text_gevonden' )

class TekstRedenAdmin( admin.ModelAdmin ):
	list_display = ( 'id', 'reden', 'reden_text' )

class TekstVoortgangAdmin( admin.ModelAdmin ):
	list_display = ( 'id', 'invoerstatus', 'invoerstatustekst' )


admin.site.register( ArchiefGemeente, ArchiefGemeenteAdmin )
admin.site.register( HsnBeheer,       HsnBeheerAdmin )
admin.site.register( HsnIdmut,        HsnIdmutAdmin )
admin.site.register( HsnKwyt,         HsnKwytAdmin )
admin.site.register( Hsnrp,           HsnrpAdmin )
admin.site.register( Huwknd,          HuwkndAdmin )
admin.site.register( Mail,            MailAdmin )
admin.site.register( Ovlknd,          OvlkndAdmin )
admin.site.register( Pkknd,           PkkndAdmin )
admin.site.register( Plaats,          PlaatsAdmin )

admin.site.register( TekstFaseA,     TekstFaseAAdmin )
admin.site.register( TekstFaseB,     TekstFaseBAdmin )
admin.site.register( TekstFaseCD,    TekstFaseCDAdmin )
admin.site.register( TekstGevonden,  TekstGevondenAdmin )
admin.site.register( TekstReden,     TekstRedenAdmin )
admin.site.register( TekstVoortgang, TekstVoortgangAdmin )

# [eof]
