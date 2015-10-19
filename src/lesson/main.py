# lesson/main.py
#
# This file is part of LESSON.  LESSON is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2 or later.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright (C) 2012 Jonathan Dieter <jdieter@lesbg.com>

import sys, os

abspath = os.path.dirname(os.path.abspath(__file__))
if abspath not in sys.path:
    sys.path.append(abspath)
os.chdir(abspath)

import render

mode = "debug"

if __name__.startswith('_mod_wsgi_'):
    print "Detected mod_wsgi; running in WSGI mode"
    mode = "wsgi"
else:
    print "Running in debug mode"

application = render.start(mode)
