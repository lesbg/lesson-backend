# lesson/controller/log.py
#
# Logging class for LESSON backend
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

from model.core import Log as DBLog, LogIgnoreHost

NONE  = 0
ERROR = 1
INFO  = 3
DEBUG = 10
class Log:
    """
    There should be one instance of this class used in the LESSON backend.
    This class is used for logging backend page access.
    """
    
    def __init__(self, db):
        self.db = db
        
    def log(self, ctx, page, username, level, comment, record_level=INFO):
        if level < 1:
            raise ValueError("Log level can't be log.NONE or negative")

        session = self.db.create_session()
                
        if not 'REMOTE_HOST' in  ctx.environ.keys():
            remote_host = ctx.environ['REMOTE_ADDR'];
        else:
            remote_host = ctx.environ['REMOTE_HOST'];
            
        # Always return 'localhost' for 127.0.0.1 and ::1
        if ctx.environ['REMOTE_ADDR'] in ("127.0.0.1", "::1"):
            remote_host = 'localhost'
        
        if 'HTTP_X_FORWARDED_FOR' in ctx.environ.keys():    
            query = session.query(LogIgnoreHost)
            for item in query:
                if item.HostAddr == remote_host:
                    remote_host = None
            if remote_host is None:
                remote_host = ctx.environ['HTTP_X_FORWARDED_FOR']
            else:
                remote_host = '%s via %s' % (remote_host, ctx.environ['HTTP_X_FORWARDED_FOR'])
        
        
        if level <= record_level:
            new_log = DBLog(page, username, level, remote_host, comment)
            session.add(new_log)
            session.commit()
            session.close()
        print page, username, level, remote_host, comment
        