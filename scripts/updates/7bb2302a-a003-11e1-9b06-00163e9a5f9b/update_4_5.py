"""
update_4_5

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

Copyright (C) 2015 Jonathan Dieter <jdieter@lesbg.com>
"""

uuid = u'7bb2302a-a003-11e1-9b06-00163e9a5f9b'
old_version = 4
new_version = 5

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, MetaData
from sqlalchemy import Column, Integer, Unicode, UnicodeText, Boolean

Base = declarative_base()

class Family(Base):
    __tablename__ = u'family'
    
    FamilyCode = Column(Unicode(50), nullable=False, primary_key=True)
    FamilyName = Column(UnicodeText, nullable=False, index=True)
    FatherName = Column(UnicodeText, index=True)
    MotherName = Column(UnicodeText, index=True)
    
class Phone(Base):
    __tablename__ = u'phone'
    
    PhoneIndex = Column(Integer, nullable=False, primary_key=True)
    Number = Column(Unicode(50), nullable=False, index=True)
    FamilyCode = Column(Unicode(50), nullable=False, index=True)
    Relationship = Column(Integer, index=True)
    Type = Column(Integer, index=True)
    Comment = Column(UnicodeText, index=True)

class User_Old(Base):
    __tablename__ = u'user'

    Username = Column(Unicode(50), nullable=False, primary_key=True)
    FirstName = Column(Unicode(50), nullable=False, index=True)
    Surname = Column(Unicode(50), nullable=False, index=True)
    Gender = Column(Unicode(1), index=True)
    PhoneNumber = Column(Unicode(20))
    CellNumber = Column(Unicode(20))
    DOB = Column(Date)
    Password = Column(String(255))
    Password2 = Column(String(255))
    Permissions = Column(Integer, default=0, nullable=False, index=True)
    Title = Column(Unicode(10))
    House = Column(Unicode(1), index=True)
    Email = Column(Unicode(256))
    DateType = Column(Integer)
    DateSeparator = Column(Unicode(1))
    ActiveStudent = Column(Integer, default=0, nullable=False, index=True)  # boolean
    ActiveTeacher = Column(Integer, default=0, nullable=False, index=True)  # boolean
    SupportTeacher = Column(Integer, default=0, nullable=False, index=True)  # boolean
    DepartmentIndex = Column(Integer, index=True)
    User1 = Column(Integer, index=True)  # boolean
    User2 = Column(Integer, index=True)  # boolean
    User3 = Column(Integer, index=True)  # boolean
    User4 = Column(Integer, index=True)  # boolean
    User5 = Column(Integer, index=True)  # boolean
        
class User_New(Base):
    __tablename__ = u'user2'

    Username = Column(Unicode(50), nullable=False, primary_key=True)
    FamilyCode = Column(Unicode(50), index=True)
    FirstName = Column(Unicode(50), nullable=False, index=True)
    Surname = Column(Unicode(50), nullable=False, index=True)
    Gender = Column(Unicode(1), index=True)
    PhoneNumber = Column(Unicode(20))
    CellNumber = Column(Unicode(20))
    DOB = Column(Date)
    Password = Column(String(255))
    Password2 = Column(String(255))
    Permissions = Column(Integer, default=0, nullable=False, index=True)
    Title = Column(Unicode(10))
    House = Column(Unicode(1), index=True)
    Email = Column(Unicode(256))
    DateType = Column(Integer)
    DateSeparator = Column(Unicode(1))
    ActiveStudent = Column(Integer, default=0, nullable=False, index=True)  # boolean
    ActiveTeacher = Column(Integer, default=0, nullable=False, index=True)  # boolean
    SupportTeacher = Column(Integer, default=0, nullable=False, index=True)  # boolean
    DepartmentIndex = Column(Integer, index=True)
    User1 = Column(Integer, index=True)  # boolean
    User2 = Column(Integer, index=True)  # boolean
    User3 = Column(Integer, index=True)  # boolean
    User4 = Column(Integer, index=True)  # boolean
    User5 = Column(Integer, index=True)  # boolean
    
def upgrade(db):
    precheck_upgrade(db)  # Must be at beginning of upgrade script

    Base.metadata.create_all(db.engine)
    User_New.__table__.insert().from_select(User_Old.__table__.select())

    version_upgrade(db)  # Must be at end of upgrade script, and only run after
                         # upgrade is successful

def downgrade(db):
    precheck_downgrade(db)  # Must be at beginning of downgrade script

    Base.metadata.drop_all(db.engine)

    version_downgrade(db)  # Must be at end of upgrade script, and only run
                           # after downgrade is successful

# #######################################
# #### Ignore everything below this #####
# #######################################
from sqlalchemy.sql import select

metadata = MetaData()

version = Table(u'version', metadata,
                Column(u'UUID', Unicode(36), nullable=False, primary_key=True),
                Column(u'Type', Unicode(50), nullable=False),
                Column(u'VersionNumber', Integer, nullable=False)
                )

def precheck_upgrade(db):
    if not _check_old(db):
        raise ValueError(u"Database doesn't match version to be upgraded")

def version_upgrade(db):
    _upgrade_version(db)
    if not _check_new(db):
        raise ValueError(u"Updated database doesn't match version to be upgraded to")

def precheck_downgrade(db):
    if not _check_new(db):
        raise ValueError(u"Database doesn't match version to be downgraded")

def version_downgrade(db):
    _downgrade_version(db)
    if not _check_old(db):
        raise ValueError(u"Updated database doesn't match version to be downgraded to")

def _check_old(db):
    result = db.engine.execute(select([version], version.c.UUID == uuid))
    if result.fetchone()[u'VersionNumber'] != old_version:
        return False
    return True

def _check_new(db):
    result = db.engine.execute(select([version], version.c.UUID == uuid))
    if result.fetchone()[u'VersionNumber'] != new_version:
        return False
    return True

def _upgrade_version(db):
    db.engine.execute(version.update().where(version.c.UUID == uuid).values(VersionNumber=new_version))

def _downgrade_version(db):
    db.engine.execute(version.update().where(version.c.UUID == uuid).values(VersionNumber=old_version))

if __name__ == "__main__":
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    class Session(object):
        def __init__(self, engine, **engine_opts):
            self.engine = create_engine(engine, **engine_opts)
            self.create_session = sessionmaker(bind=self.engine)

    db = Session(u'sqlite://')
    version.create(db.engine)
    db.engine.execute(version.insert().values(UUID=uuid, Version=old_version, Type=u""))
    upgrade(db)
    downgrade(db)
    result = db.engine.execute(select([version], version.c.UUID == uuid))
    if result.fetchone()[u'VersionNumber'] != old_version:
        raise ValueError(u"After upgrade/downgrade process, database has been changed")

