# lesson/version.py
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

from model.core import Version
import subprocess, os.path
import sys, traceback

class VersionCheck(object):
    """
    Version is a virtual class that will check whether the database version
    of a module matches the current version of the module

    If the database version is less than the module version, Version will
    attempt to run any update files in <script_dir> in the form of
    (uuid)-update-(old version)-(new version) when auto_update is True

    If the versions differ by more than one, the class will check for the
    existence of intermediate update files and run them if applicable

    Child classes *must* specify uuid and module version (version).  Child
    classes may also specify update script directory (script_dir) for automatic
    database updates, as well as turning off automatic database updates by
    setting auto_update to False

    You do not need to actually run the check, as the backend will do so
    automatically when it starts up.
    """
    db = None
    uuid = None
    script_dir = None
    version = None
    auto_update = True
    extension = 'sh'

    def __init__(self, db, script_dir=None):
        if self.__class__.__name__ == "VersionCheck":
            raise ValueError("'VersionCheck' is a virtual class and should not be instantiated directly")
        self.db = db
        self.script_dir = script_dir

    def check_file(self, ufile):
        """
        Check whether update file exists.  Return True if file exists, False
        if it doesn't.  This function may be overridden if desired
        """
        if os.path.exists(ufile):
            return True
        return False

    def run_file(self, ufile):
        """
        Run an update file and return True if update was successful, False if
        it wasn't successful.  This function may be overridden if desired
        """
        try:
            messages = subprocess.check_output(ufile, stderr=subprocess.STDOUT, shell=True) #@UnusedVariable
            return (True, None)
        except:
            return (False, u"Error running %s" % (ufile,))

    def __check_file(self, start_ver, stop_ver):
        ufile = os.path.join("%s" % (self.script_dir,),
                             "%s-update-%i-%i.%s" % (self.uuid, start_ver, stop_ver, self.extension))

        # Check whether update exists for start_ver -> stop_ver
        if self.check_file(ufile):
            return [ufile]

        # Version jump is > 1, so split version jump in half and recursively
        # check for updates for each half 
        elif start_ver + 1 < stop_ver:
            filelist = []
            middle = ((stop_ver - start_ver) / 2) + start_ver

            for item in self.__check_file(start_ver, middle):
                if item is None:
                    return [None]
                filelist.append(item)
            for item in self.__check_file(middle, stop_ver):
                if item is None:
                    return [None]
                filelist.append(item)
            return filelist

        # No updates for this start_ver -> stop_ver, so return [None]
        else:
            return [None]

    def check_version(self):
        """
        Returns a tuple of (boolean, string|None) where the boolean is
        whether the versions match and the string is the error message
        if they don't match
        """
        print "Checking..."
        if self.db is None:
            raise ValueError("Database variable 'db' isn't set")
        if self.uuid is None:
            raise ValueError("UUID variable 'uuid' isn't set")
        session = self.db.create_session()
        cur_ver = session.query(Version).get(self.uuid)
        session.close()
        if cur_ver.VersionNumber > self.version:
            return (False, u"The %s version in the database is %i, while our version is %i.  Please upgrade module %s" % (cur_ver.Type, cur_ver.Version, self.version, cur_ver.Type))
        elif cur_ver.VersionNumber < self.version:
            script_files = [None]
            if self.script_dir is not None:
                script_files = self.__check_file(cur_ver.VersionNumber, self.version)
            if script_files == [None]:
                return (False, u"The %s version in the database is %i, while our version is %i.  Please manually upgrade the database for %s" % (cur_ver.Type, cur_ver.Version, self.version, cur_ver.Type))
            for ufile in script_files:
                retval, error = self.run_file(ufile)
                if not retval:
                    return (False, error)
        return (True, None)

class PyVersionCheck(VersionCheck):
    extension = 'py'

    def __init__(self, db, script_dir):
        if self.__class__.__name__ == "PyVersionCheck":
            raise ValueError("'PyVersionCheck' is a virtual class and should not be instantiated directly")
        super(PyVersionCheck, self).__init__(db, script_dir)

    def run_file(self, ufile):

        import imp
        uname = os.path.basename(ufile)
        if ufile.endswith('.py'):
            uname = uname[:-3]
        try:
            f = open(ufile, 'U')
        except:
            return (False, u"Error opening %s" % (ufile,))
        try:
            upgrade = imp.load_module('upgrade', f, ufile, ('.py', 'U', 1))
            upgrade.upgrade(self.db)
            session = self.db.create_session()
            cur_ver = session.query(Version).get(self.uuid)
            session.close()
            if cur_ver.VersionNumber != self.version:
                return (False, u"Module %s didn't upgrade version in database" % (ufile,))
            return (True, None)
        except:
            for item in traceback.format_exception(*sys.exc_info()):
                print item
            return (False, u"Error loading update module %s" % (ufile,))
        finally:
            f.close()
