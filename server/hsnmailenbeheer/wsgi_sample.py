# -*- coding: utf-8 -*-

"""
FL-03-Jun-2015	Created
FL-17-Nov-2015	Changed

WSGI config for hsnmailenbeheer project.
It exposes the WSGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/

Use this file wsgi_sample.py to create a new file wsgi.py in the same directory. 
And replace the 2 strings below with their actual paths:
	<path_to_virtual_python_installation>
	<path_to_hsnmailenbeheer>
"""

from os import environ
from sys import path, version


# setup the virtual environment
activate_this = "<path_to_virtual_python_installation>/python2710/bin/activate_this.py"

execfile( activate_this, dict( __file__ = activate_this ) )
print( version )

# additions to used python; prepend to path
path.insert( 0, "<path_to_hsnmailenbeheer>/hsnmailenbeheer/server" )			# project parent dir
path.insert( 0, "<path_to_hsnmailenbeheer>/hsnmailenbeheer/server/hsnmailenbeheer" )	# project root dir, containing settings.py

environ.setdefault( "DJANGO_SETTINGS_MODULE", "hsnmailenbeheer.settings" )

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# [eof]
