uuid = u"7bb2302a-a003-11e1-9b06-00163e9a5f9b"
old_version = 1
new_version = 2

def get_metadata():
    from sqlalchemy.ext.declarative import declarative_base
    
    Base = declarative_base()
    
    class LogIgnoreHost(Base):
        __tablename__ = u'log_ignore_host'
        
        LogIgnoreHostIndex = Column(Integer, nullable=False, primary_key=True)
        HostAddr           = Column(Unicode(32), nullable=False)

    return Base

def upgrade(db):
    precheck_upgrade(db) # Must be at beginning of upgrade script 
    
    Base = get_metadata()    
    Base.metadata.create_all(db.engine)
    
    version_upgrade(db) # Must be at end of upgrade script, and only run after
                        # upgrade is successful 

    
def downgrade(db):
    precheck_downgrade(db) # Must be at beginning of downgrade script 
    
    Base = get_metadata()    
    Base.metadata.drop_all(db.engine)
    
    version_downgrade(db) # Must be at end of upgrade script, and only run
                          # after downgrade is successful 

########################################
##### Ignore everything below this #####
########################################
from sqlalchemy import Table, MetaData
from sqlalchemy import Column, Integer, Unicode

from sqlalchemy.sql import select

metadata = MetaData()

version = Table(u'version', metadata,
                Column(u'UUID',    Unicode(36), nullable=False, primary_key=True),
                Column(u'Type',    Unicode(50), nullable=False),
                Column(u'Version', Integer,     nullable=False)
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
    if result.fetchone()[u'Version'] != old_version:
        return False
    return True

def _check_new(db):
    result = db.engine.execute(select([version], version.c.UUID == uuid))
    if result.fetchone()[u'Version'] != new_version:
        return False
    return True
    
def _upgrade_version(db):
    db.engine.execute(version.update().where(version.c.UUID==uuid).values(Version=new_version))
    
def _downgrade_version(db):
    db.engine.execute(version.update().where(version.c.UUID==uuid).values(Version=old_version))
    
if __name__ == "__main__":
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    
    class Session(object):
        def __init__(self, engine, **engine_opts):
            self.engine = create_engine(engine, **engine_opts)
            self.create_session = sessionmaker(bind=self.engine) 
    
    db = Session(u'sqlite://')
    version.create(db.engine)
    db.engine.execute(version.insert().values(UUID=uuid, Version=old_version, Type=""))
    upgrade(db)
    downgrade(db)
    result = db.engine.execute(select([version], version.c.UUID == uuid))
    if result.fetchone()[u'Version'] != old_version:
        raise ValueError("After upgrade/downgrade process, database has been changed")
