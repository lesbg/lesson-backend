# lesson/controller/config.py
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

import ConfigParser, os, sys

def get_config():
    """
    Get LESSON configuration, creating it if it doesn't already exist
    """
    config_path = None
    for path in ('config/lesson.conf', '/etc/lesson.conf'):
        if os.path.exists(path):
            config_path = path
            break
    if config_path is None:
        create_config('config/lesson.conf')
        config_path = 'config/lesson.conf'
    config = ConfigParser.SafeConfigParser()
    try:
        config.read(config_path)
    except:
        print u"ERROR: Unable to read configuration file at %s" % (config_path,)
        sys.exit(1)
    return config
            
def create_config(path):
    """
    Create configuration file at path
    """
    config = ConfigParser.RawConfigParser()
    config.add_section('Main')
    config.set('Main', 'database',
               u'mysql+mysqldb://test.example.com/lesson?charset=utf8')
    config.set('Main', 'script dir', u'scripts')
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path), 0700)
        except:
            print u"ERROR: Unable to create directory '%s' for configuration file." % (os.path.dirname(path),)
            sys.exit(1)
    try:
        configfile = open(path, 'wb')
    except:
        print u"ERROR: Unable to open configuration file '%s' for writing." % (path,)
        sys.exit(1)
    config.write(configfile)
    configfile.close()
        