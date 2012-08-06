# lesson/permission.py
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

class Permission:
    def __init__(self, user):
        self.user = user
        
    # Currently, most of this is hard-coded.  I hope to change this to a proper
    # permissions-based table in LESSON
    def has_permission(self, permission, to_check=None):
        # New permissions should be added in the following way:
        # elif permission == "some_permission":
        #     if user matches some_condition:
        #         return True
        #     elif user matches some_other_condition:
        #         return True
        #     return False
        
        # Admin only permissions
        if permission in ["list_users", "show_log", "show_year", "show_departments", "show_attributes"]:
            if self.user.Permissions == 1:
                return True
            return False
        
        if permission == "user_info":
            if self.user.Permissions == 1:
                return True
            if self.user.Username == to_check['Username']:
                return True
            return False
        return False