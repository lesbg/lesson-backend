# lesson/password.py
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

import hashlib
from passlib.apps import ldap_context
ldap_context = ldap_context.replace(default="ldap_sha512_crypt")

def encrypt(password):
    return ldap_context.encrypt(password)

def validate(password, pwhash):
    
    # Check for old-style MD5 passwords which won't have any associated type
    if pwhash[0] != "{":
        if hashlib.md5(password).hexdigest() == pwhash:
            return True
        else:
            return False
    else:
        return ldap_context.verify(password, pwhash)
