#!/bin/sh
/usr/sbin/cupsd
exec /usr/sbin/httpd -D FOREGROUND
