from os import environ
from sys import path, version

activate_this = "/app/venv/bin/activate_this.py"

execfile( activate_this, dict( __file__ = activate_this ) )
print( version )

# additions to used python; prepend to path
path.insert( 0, "/app/server" )			# project parent dir
path.insert( 0, "/app/server/hsnmailenbeheer" )	# project root dir, containing settings.py

environ.setdefault( "DJANGO_SETTINGS_MODULE", "hsnmailenbeheer.settings" )

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
