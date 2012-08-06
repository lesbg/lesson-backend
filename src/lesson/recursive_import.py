# lesson/import.py
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

import os, sys

def get_import_path(module_path):
    if module_path in sys.path:
        return module_path
    else:
        return get_import_path(os.path.dirname(module_path))
    
def get_import_module(module_name):
    import_path = get_import_path(module_name)
    module_name = module_name.replace(import_path, "")
    module_name = module_name.strip("/")
    module_name = module_name.replace("/", ".")
    return module_name

def recursive_import(module_location):
    module_dir = os.path.dirname(module_location)
    for filename in os.listdir(module_dir):
        name, ext = os.path.splitext(filename)
        module_file = os.path.join(module_dir, filename, "__init__.py")
        if os.path.exists(module_file):
            module_name = get_import_module(os.path.join(module_dir, filename))    
            __import__(module_name)
            recursive_import(module_file)
        elif ext == ".py" and name != "__init__":
            module_name = get_import_module(os.path.join(module_dir, name))
            __import__(module_name)