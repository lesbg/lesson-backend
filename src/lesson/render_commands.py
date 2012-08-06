# lesson/render_commands.py
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

try:
    import simplejson as json
except ImportError:
    import json
    
from urlparse import urlparse

import xmlrpclib
import datetime
    
def is_listish(obj):
    return ((hasattr(obj, "__getitem__") and
               not hasattr(obj, "strip")) or
                   hasattr(obj, "__iter__"))

def urlize(string):
    try:
        url = urlparse(string, allow_fragments=False)
    except:
        return string
    if url[1] == "": # Netloc is empty, not a url
        return string
    return u"<a href='%s'>%s</a>" % (string, string)

def get_header(line, header_sep, row_sep, quote_str, create_links):
    retval = ""
    if hasattr(line, 'keys'):
        retval = header_sep[0]
        for key in line.keys():
            if create_links:
                key = urlize(key)
            if quote_str != "" and (isinstance(key, str) or isinstance(key, unicode)):
                key = quote_str + key.replace(quote_str, "\\" + quote_str) + quote_str
            retval += unicode(key) + header_sep[1]
        retval = retval[:-len(header_sep[1])] + header_sep[2]
        retval += row_sep[1] + row_sep[0]
    return retval

def get_item(line, item_sep, quote_str, create_links):
    if hasattr(line, "values"):
        line = line.values()
    retval = item_sep[0]
    for item in line:
        if create_links:
            item = urlize(item)
        if quote_str != "" and (isinstance(item, str) or isinstance(item, unicode)):
            item = quote_str + item.replace(quote_str, "\\" + quote_str) + quote_str
        retval += unicode(item) + item_sep[1]
    retval = retval[:-len(item_sep[1])] + item_sep[2]
    return retval
    
def tablize(obj, body_start=u"", body_end=u"", row_sep=(u"", u"\n"),
            header_sep=(u"", u",", u""), item_sep=(u"", u",", u""),
            quote_str=u"", create_links=False):
        retval = body_start
        firstline = True
        if hasattr(obj, "values"):
            check_list = obj.values()
        else:
            check_list = obj
        if len(check_list) == 1 and is_listish(check_list[0]):
            check_list = check_list[0]
            obj = check_list
            if hasattr(check_list, "values"):
                check_list = check_list.values()
        if len(check_list) >= 1:
            if is_listish(check_list[0]):
                for line in obj:
                    retval += row_sep[0]
                    if firstline:
                        retval += get_header(line, header_sep, row_sep, quote_str, create_links)
                        firstline = False
                    retval += get_item(line, item_sep, quote_str, create_links)
                    retval += row_sep[1]
            else:
                retval += row_sep[0]
                retval += get_header(obj, header_sep, row_sep, quote_str, create_links)
                retval += get_item(obj, item_sep, quote_str, create_links)
                retval += row_sep[1]
        retval += body_end
        return retval

class RenderCom:
    def __init__(self):
        self.headers = True
        
    
    def __xml_fix_date(self, obj):
        if hasattr(obj, "keys"):
            objlist = obj.keys()
        else:
            objlist = obj
        count = 0
        for item in objlist:
            if hasattr(obj, "keys"):
                key = item
                item = obj[key]
            else:
                key = count
                count += 1
            if is_listish(item):
                print key
                self.__xml_fix_date(item)
            else:
                print key, item
                if not isinstance(item, datetime.datetime) and isinstance(item, datetime.date):
                    obj[key] = datetime.datetime(item.year, item.month, item.day)
            
    def json_handler(self, obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        else:
            raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj))
        
    def render_xml(self, **args):
        self.__xml_fix_date(args)
        return xmlrpclib.dumps((args,), methodresponse=True, allow_none=True)
    
    def render_json(self, **args):
        return json.dumps(args, default=self.json_handler, sort_keys=True)
    
    def render_html(self, **args):
        return tablize(args, u"<html><body><table>", u"</table></body></html>",
                       ("<tr>", "</tr>\n"), ("<th>", "</th><th>", "</th>"),
                                            ("<td>", "</td><td>", "</td>"),
                        create_links=True)
    
    def render_txt(self, **args):
        return tablize(args, u"", u"", ("", "\n"), ("", "\t", ""),
                                                    ("", "\t", ""))
    
    def render_csv(self, **args):
        return tablize(args, u"", u"", ("", "\n"), ("", ",", ""),
                                                    ("", ",", ""), "\"")
