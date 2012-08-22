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

from model.core import Config as DBConfig, uuid as core_uuid

def get_file_config():
    """
    Get LESSON configuration, creating it if it doesn't already exist
    """
    config_path = None
    for path in ('config/lesson.conf', '/etc/lesson.conf'):
        if os.path.exists(path):
            config_path = path
            break
    if config_path is None:
        create_file_config('config/lesson.conf')
        config_path = 'config/lesson.conf'
    config = ConfigParser.SafeConfigParser()
    try:
        config.read(config_path)
    except:
        print u"ERROR: Unable to read configuration file at %s" % (config_path,)
        sys.exit(1)
    return config
            
def create_file_config(path):
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

def get_config(session, uuid, key, fallback=True):
    """
    Return configuration value for pair uuid, key.  If pair uuid, key doesn't
    exist, fall back to core uuid, key.  If that doesn't exist, return None.
    
    This will *always* return a unicode string.
    """
    if isinstance(key, str):
        raise ValueError("Key '%s' is not unicode" % (key,))
    
    item = session.query(DBConfig).filter_by(UUID=uuid, Key=key).first()
    
    if item is not None:   
        return item.Value
    elif fallback:
        return get_config(session, core_uuid, key, False)
    else:
        return None
    
def set_config(session, uuid, key, value):
    """
    Sets configuration value for combination uuid, key, value.  If value
    already exists, overwrite, otherwise create new value
    """
    if isinstance(key, str):
        raise ValueError("Key '%s' is not unicode" % (key,))
        
    key = unicode(key)
    value = unicode(value)
    
    item = session.query(DBConfig).filter_by(UUID=uuid, Key=key).first()
    
    if item is not None:
        item.Value = value
    else:
        item = DBConfig(UUID=uuid, Key=key, Value=value)
        session.add(item)
    session.commit()
