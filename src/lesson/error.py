"""
error

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

Copyright (C) 2012 Jonathan Dieter <jdieter@lesbg.com>
"""

INVALID = 400 # Bad Request
UNAUTHORIZED = 401 # Unauthorized
FORBIDDEN = 403 # Forbidden
NOT_FOUND = 404 # Not Found
BAD_METHOD = 405 # Method Not Allowed
INTERNAL_ERROR = 500 # Internal Server Error

web_error = {

400: '400 Bad Request',
401: '401 Unauthorized',
403: '403 Forbidden',
404: '404 Not Found',
405: '405 Method Not Allowed',
500: '500 Internal Server Error'

}
