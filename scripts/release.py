#!/usr/bin/python
"""
release

This file is part of LESSON.  LESSON is free software: you can
redistribute it and/or modify it under the terms of the GNU General Public
License as published by the Free Software Foundation, version 2 or later.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 51
Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

Copyright (C) 2012 Jonathan Dieter <jdieter@lesbg.com>
"""

import sys
sys.path.insert(0, '../src/lesson')

from controller import config

config.create_file_config("../examples/lesson.conf")
