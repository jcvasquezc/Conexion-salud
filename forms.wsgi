#!/usr/bin/python

import sys

if sys.version_info[0]<3:       # require python3
 raise Exception("Python3 required! Current (wrong) version: '%s'" % sys.version_info)

sys.path.insert(0, '/var/www/conexionsalud/')
from forms import app as application

from map_conexion import app as application

