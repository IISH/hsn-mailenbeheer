# -*- coding: utf-8 -*-

"""
Author:		Fons Laan, KNAW IISH - International Institute of Social History
Project:	HSN Mail
Name:		admin.py
Version:	1.0.0
Goal:		Admin classes for the hsn_mail tables

26-May-2015	Created
09-Sep-2015	Missing HuwkndAdmin added
12-Oct-2015	Removed superfluous tables
27-Oct-2015	Changed
"""


from django.contrib import admin

from .models import ( ArchiefGemeente, HsnBeheer, HsnIdmut, HsnKwyt, Mail )

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

class MailAdmin( admin.ModelAdmin ):
    list_display = ( 'id', 'idnr', 'briefnr', 'aard', 'datum', 'periode', 'gemnr', 'naamgem', 'status', 
		'printdatum', 'printen', 'ontvdat', 'opmerk', 'opident', 'oppartner', 'opvader', 'opmoeder', 'type', 
		'infoouders', 'infopartner', 'inforeis' )


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
admin.site.register( Mail,            MailAdmin )

admin.site.register( TekstFaseA,     TekstFaseAAdmin )
admin.site.register( TekstFaseB,     TekstFaseBAdmin )
admin.site.register( TekstFaseCD,    TekstFaseCDAdmin )
admin.site.register( TekstGevonden,  TekstGevondenAdmin )
admin.site.register( TekstReden,     TekstRedenAdmin )
admin.site.register( TekstVoortgang, TekstVoortgangAdmin )

# [eof]
