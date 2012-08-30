# lesson/model/__init__.py
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

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, object_mapper

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Unicode

Base = declarative_base()

class Permission(Base):
    __tablename__ = u'permission'
    
    ConfigIndex = Column(Integer, nullable=False, primary_key=True)
    UUID = Column(Unicode(36), nullable=False, index=True)
    Type = Column(Unicode(50), nullable=False, index=True)
    Username = Column(Unicode(50), nullable=False, index=True)
    
class Session(object):
    def __init__(self, engine, **engine_opts):
        self.engine = create_engine(engine, **engine_opts)
        self.create_session = sessionmaker(bind=self.engine)

class TableTop(object):
    def _get_list_link(self):
        if not hasattr(self, "Link"):
            return None
        return u"%s" % (self.Link)

    def _get_obj_link(self):
        if self.get_list_link() is None:
            return None
        return u"%s/%s" % (self.Link, unicode(self.get_primary_key()[1]))

    def _get_attr_link(self):
        if self.get_obj_link() is None:
            return None
        return u"%s/attributes" % (self.get_obj_link())

    def get_list_link(self):
        return self._get_list_link()

    def get_obj_link(self):
        return self._get_obj_link()

    def get_attr_link(self):
        return self._get_attr_link()

    def get_primary_key(self):
        mapper = object_mapper(self)
        return (unicode(mapper.primary_key[0].key), mapper.primary_key_from_instance(self)[0])
    
    def check_type(self, local_list, check_list):
        """
        Go through list from locals(), verifying that variables in check_list are of
        the right type.
        """
        for item in check_list:
            name = item[0]
            check_type = item[1]
            if len(item) > 2:
                allow_none = item[2]
            else:
                allow_none = True
            try:
                obj = local_list[name]
            except:
                raise NameError("Variable '%s' doesn't exist" % (name,))
            print name, obj, check_type
            if not isinstance(obj, check_type):
                if allow_none:
                    if obj is None:
                        continue
                    else:
                        raise TypeError("'%s' must be %s or 'None'" % (name, check_type.__name__))
                else:
                    raise TypeError("'%s' must be %s" % (name, check_type.__name__))
                    
            
    def has_permission(self, user):
        pass