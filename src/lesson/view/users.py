# lesson/view/users.py
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

uuid = u'7bb2302a-a003-11e1-9b06-00163e9a5f9b'

from render import ObjectPage, AttrPage
from model.core import User

class UserPage(ObjectPage):
    url = "/users/([^/]*)"
    
    def get(self, username):
        # Check whether we have permission to access this user's information
        if not self.validator.has_permission('user_info', username):
            return self.forbidden()

        userlist = []
        userlist.append({u'name': u'attributes', u'link': self.gen_link("users/%s/attributes" % (username,))})
        return {u'user': userlist}
        
class UserAttrPage(AttrPage):
    url = "/users/([^/]*)/attributes"
    table = User

    def get(self, username):
        # Check whether we have permission to access this user's information
        if not self.validator.has_permission('user_info', username):
            return self.forbidden()
        
        # Get current user attributes
        #user = self.db.session.query(User).filter_by(Username=username).first()
        return self._get(username)