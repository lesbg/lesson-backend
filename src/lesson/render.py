# lesson/render.py
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

import web, re, base64, os.path
import mimerender
import sqlalchemy.orm
from sqlalchemy.orm import class_mapper, object_mapper, aliased

from render_commands import RenderCom
import model
from controller import password
from controller.permission import Permission

import controller.core_version #@UnusedImport

from controller import log

import sys

from version import VersionCheck

from model.core import User

from error import *

from controller import config

from recursive_import import recursive_import

mimerender = mimerender.WebPyMimeRender()

url_dict = {}
urls = []

DEBUG = True

class _GlobalData:
    def __init__(self):
        # self.session = None
        # self.store = None
        self.rendercom = None
        self.config = config.get_config()
        self.engine = unicode(self.config.get('Main', 'database'))
        self.script_dir = self.config.get('Main', 'script dir')
        self.db = model.Session(self.engine, pool_recycle=3600)
        self.log = log.Log(self.db)

_global_data = _GlobalData()
_global_data.rendercom = RenderCom()

def __urls_from_url_dict():
    del urls[:]
    templist = []
    for path, value in url_dict.items():
        if value[2]:
            templist.append((value[0], path, value[1]))
        else:
            templist.append((value[0], '/?(.*)' + path, value[1]))
            #urls.append('/?(.*)' + path)
    templist.sort()
    for (order, path, module) in templist:
        print order, path, module
        urls.append(path) 
        urls.append(module)
    return

def _append_url(string, priority, module, name, absolute):
    if not hasattr(string, 'strip'):
        raise ValueError('URL pattern must be a string or unicode string')
    else:
        if url_dict.has_key(string):
            if url_dict[string][0] <= priority:
                return
            if DEBUG:
                print 'Replacing class for location %s' % (string,)
                print '  %s -> %s.%s' % (url_dict[string][1], module, name)
                    
    url_dict[string] = (priority, '%s.%s' % (module, name), absolute)
    return

def _is_listish(obj):
    if ((hasattr(obj, '__getitem__') and
               not hasattr(obj, 'strip')) or
                   hasattr(obj, '__iter__')):
        return True
    else:
        return False
    
def _die_on_string(obj):
    if(_is_listish(obj)):
        if hasattr(obj, 'values'):
            for item in obj.values():
                _die_on_string(item)
            if hasattr(obj, 'keys'):
                for item in obj.keys():
                    _die_on_string(item)
        else:
            for item in obj:
                _die_on_string(item)
    else:
        if isinstance(obj, str):
            raise ValueError('All strings must be unicode strings')
    
def start(mode):
    app = web.application(urls, globals())
    if mode == "debug":
        app.run()
    elif mode == "wsgi":
        application = app.wsgifunc()
        return application
    else:
        print "ERROR: Unknown mode: %s" % (mode,)
        sys.exit(1)

class _ActionMetaClass(type):
    def __init__(klass, name, bases, attrs): #@NoSelf
        if attrs.has_key('url'):
            obj = attrs['url']
            priority = None
            if attrs.has_key('priority'):
                priority = attrs['priority']
            else:
                for base in bases:
                    if base.__dict__.has_key('priority'):
                        priority = base.__dict__['priority']
                if priority is None:
                    priority = 0
            if attrs.has_key('url_absolute'):
                absolute = attrs['url_absolute']
            else:
                absolute = False
            if ((hasattr(obj, '__getitem__') and not hasattr(obj, 'strip')) or
                 hasattr(obj, '__iter__')):
                if hasattr(obj, 'values'):
                    for item in obj.values():
                        _append_url(item, priority, klass.__module__, name, absolute)
                else:
                    for item in obj:
                        _append_url(item, priority, klass.__module__, name, absolute)
            else:
                _append_url(obj, priority, klass.__module__, name, absolute)
    
class Page:
    
    __metaclass__ = _ActionMetaClass
    
    table = None
    priority = 80
    user = None
    check_vars = True
    permission_args = {}
    offset = 0
    limit = 100
    base_link = None
    prefix = None
    query = None
    errno = None
    error = None
    error_level = None
    log_error = True
    status = None
    session = None
    
    def __init__(self):
        self.db  = _global_data.db
        self._log = _global_data.log
    
    def log(self, comment, level = None, username = None):
        if username is None:
            username = self.user.Username
        if level is None:
            level = log.DEBUG
        self._log.log(web.ctx, web.ctx.fullpath.replace("/" + self.prefix + "/", ""), username, level, comment)
        
    @mimerender(
        default = 'html',
        override_input_key = 'format',
        html = _global_data.rendercom.render_html,
        xml  = _global_data.rendercom.render_xml,
        json = _global_data.rendercom.render_json,
        txt  = _global_data.rendercom.render_txt,
        csv  = _global_data.rendercom.render_csv
    )
    def _render(self, *args, **kwargs):
        if self.errno is not None:
            self.error = unicode(self.error)
            if web_error.has_key(self.errno):
                self.status = web_error[self.errno]
            else:
                self.status = web_error[400]
                self.error += u'\nIn addition, the web server return unknown error code %i' % (self.errno,)
            if self.log_error:
                self.log(self.error, self.error_level)
            return {'errno': unicode(self.status), 'error': self.error}
        if len(args) == 1:
            if self.check_vars:
                _die_on_string(args[0])
            if args[0] is None:
                return {}
            return args[0]
        else:
            raise ValueError('Too many arguments.  This should be impossible')
    
    def logged(self):
        auth = web.ctx.env.get('HTTP_AUTHORIZATION') #@UndefinedVariable
        if auth is None:
            return False
        else:
            auth = re.sub('^Basic ','',auth)
            username,passwd = base64.decodestring(auth).split(':')
            user = self.session.query(User).filter_by(Username=username).first()
            if user is None:
                self.log(u"Non-existent username: %s" % (username,), log.ERROR, username)
                return False
            if not password.validate(passwd, user.Password):
                self.log(u"Invalid password for username: %s" % (username,), log.ERROR, username)
                return False
            self.user = user
            self.validator = Permission(user)
            
            return True
    
    def gen_link(self, page):
        """
        Generate absolute url from app relative url
        """
        if page.startswith('/'):
            page = page[1:]
        page = '%s/%s' % (web.ctx.home, page)
        return page        
    
    def check_permissions(self):
        if not self.logged():
            web.header('WWW-Authenticate','Basic realm="LESSON login"')
            self.errno     = UNAUTHORIZED
            self.error     = u"You must log in before accessing this page"
            self.log_error = False
            return
        if hasattr(self, 'permission') and not self.validator.has_permission(self.permission, self.permission_args):
            self.errno       = FORBIDDEN
            self.error       = u"Access to this page is denied"
            self.error_level = log.ERROR
            return
        return None
        
    def _strip_prefix(self, args, kwargs):
        if len(args) > 0:
            self.prefix = args[0]
            args = tuple(args[1:])
            
        elif kwargs.has_key('prefix'):
            self.prefix = kwargs['prefix']
            del kwargs['prefix']
            
        # Strip leading and trailing slashes from prefix
        if self.prefix is None:
            self.prefix = u""
        self.prefix = self.prefix.strip('/')
        
        return args, kwargs
    
    def __split_url_segment(self, segment):
        """
        Split a url segment in form table@link_table#key into tuple of (table,
        link_table, key) where link_table and key may be None
        """
        
        # This would probably be easier as a regex, but I have no idea how to
        # make this work where the order of link_table and key doesn't matter
        x = segment.find('@')
        y = segment.find('$')
        link_table = None
        key       = None
        if x > -1:
            if x < y:
                link_table = segment[x + 1:y]
            else:
                link_table = segment[x + 1:]
        if y > -1:
            if y < x:
                key = segment[y + 1: x]
            else:
                key = segment[y + 1:]
        
        table = segment
        if x > -1 and (x < y or y == -1):
            table = segment[:x]
        elif y > -1 and (y < x or x == -1):
            table = segment[:y]
            
        return (table, link_table, key)
    
    def __build_filter_url(self):
        """
        Build filter url from filters.  If filters has been run through
        self._gen_default_query, filter url is canonical.
        """
        filter_url = ""
        for ffilter in self.filters:
            filter_url += "/" + ffilter['table']
            if ffilter['link_table'] is not None:
                filter_url += "@" + ffilter['link_table']
            if ffilter['key'] is not None:
                filter_url += "$" + ffilter['key']
            filter_url += "/" + ffilter['value']
        return filter_url[1:]
    
    def _get_filters(self):
        """
        Work out SQL filters from self.prefix with very little error checking
        """
        filter_list = self.prefix.split('/')
        self.filters = []
        
        if filter_list == [u'']:
            return
        
        step = 1
        for item in filter_list:
            if step == 1:
                # Extract link table and key from link section
                (table, link_table, key) = self.__split_url_segment(item)
                
                for x in model.TableTop.__subclasses__(): #@UndefinedVariable
                    if hasattr(x, "Link") and x.Link == table:                        
                        self.filters.append({'table_class': x, 'table': table, 'link_table': link_table, 'key': key})
                        step = 2
                if step != 2: # We didn't find any tables that matched
                    self.errno = 400
                    self.error = u"Table %s isn't in database" % (table,)
                    return None
                else:
                    continue
            if step == 2:
                self.filters[-1]['value'] = item
                step = 1
        
    def _gen_default_query(self):
        """
        Generate default query from self.table and filters.  Default query is
        stored in self.query, and there is no return value.  This also
        normalizes the filter list stored in self.filters and redirects if
        filter list isn't canonical.
        """

        if self.table is None:
            self.query = None
            return
        
        self.filters.reverse()
        query = self.session.query(self.table)
        
        used_table_list = [(class_mapper(self.table), self.table)]
        for item in self.filters:
            if item['link_table'] is not None and hasattr(used_table_list[0][1], "Link") and item['link_table'] == used_table_list[0][1].Link:
                item['link_table'] = None
                
            foreign_key = None
            table = class_mapper(item['table_class'])
            
            # Get linked table in relationship
            link_table = None
            if item['link_table'] is None:
                link_table = used_table_list[0][0]
                link_table_class = used_table_list[0][1]
            else:
                found = False
                for test_table in used_table_list:
                    if test_table[1].Link == item['link_table']:
                        link_table_class = test_table[1]
                        link_table = test_table[0]
                        found = True
                if not found:
                    self.query = False
                    self.errno = 400
                    self.error = u"Unable to find link table %s" % item['link_table']
                    return
            
            # Create alias if link_table is linked multiple times
            for old_table in used_table_list:
                if old_table[1] == item['table_class']:
                    item['table_class'] = aliased(item['table_class'])
                    
            used_table_list.insert(0, (table, item['table_class']))
            
            # Get primary key in relationship
            count = 0
            for x in link_table.iterate_properties:
                if isinstance(x, sqlalchemy.orm.properties.RelationshipProperty):
                    if x.remote_side[0] == table.primary_key[0]:
                        count += 1
                        if item['key'] is not None:
                            if item['key'] == unicode(x.local_side[0].key):
                                foreign_key = getattr(link_table_class, x.local_side[0].key)
                                if item['key'] == unicode(x.remote_side[0].key):
                                    item['key'] = None
                        else: # No specified key
                            foreign_key = getattr(link_table_class, x.local_side[0].key)
                            if count > 1:  # More than one possible relationship, so don't return any
                                self.errno = 400
                                self.error = "There are multiple possible relationships between column %s in table %s and table %s" % (table.primary_key[0].key, item['table_class'].Link, link_table_class.Link)
                                return
            if foreign_key is None:
                self.errno = 400
                self.error = "There's no relationship between column %s in table %s and table %s" % (table.primary_key[0].key, item['table_class'].Link, link_table_class.Link)
                return 
            
            primary_key = getattr(item['table_class'], table.primary_key[0].key)     
            query = query.join(item['table_class'], primary_key == foreign_key).filter(primary_key == item['value'])
        self.filters.reverse()

        # Verify that current filter path is canonical.  If not, redirect to
        # canonical path
        filter_url = self.__build_filter_url()
        if self.prefix != filter_url:
            full_path = web.ctx.path[1:]
            full_path = full_path.replace(self.prefix, '')
            print 'Redirecting to /' + filter_url + full_path
            web.seeother('/' + filter_url + full_path)

        self.query = query

    def _set_status(self, procedure, args, kwargs):
        """
        Set self.status to current web.ctx.status, then after page has been
        rendered, set web.ctx.status to updated self.status.  This is needed
        for old web.py (0.32).
        """
        self.status = web.ctx.status
        retval = self._parse(procedure, args, kwargs)
        web.ctx.status = self.status
        return retval
    
    def _parse(self, procedure, args, kwargs):
        # Open database session
        self.session = self.db.create_session()
        
        (args, kwargs) = self._strip_prefix(args, kwargs)
        
        # Check permissions
        self.check_permissions()
        
        # Immediately exit if we've hit a permissions error
        if self.errno is not None:
            return self._render()
        
        # Verify that prefix is in multiples of two
        if len(self.prefix.split('/')) % 2 != 0 and self.prefix != '':
            self.errno = 400
            self.error = u"Filters must be in the form /table[@linktable][$foreign_key]/primary_key, but yours is %s" % (self.prefix,)
            return self._render()
        
        # Verify that prefix is a valid filter
        self._get_filters()
        if self.errno is not None:
            return self._render()
        
        # Generate default query
        self._gen_default_query()
        if self.errno is not None:
            return self._render()
        
        retval = self._render(procedure(*args, **kwargs))
        self.log("Accessed page")
        
        # Close database session
        self.session.close()            
        return retval
            
    # Pseudo-procedures for base class page.  These should be overridden by any
    # child classes
    def get(self):
        self.errno = BAD_METHOD
        self.error = u"GET method doesn't exist for page class %s" % (self.__class__.__name__,)
        return
    
    def push(self):
        self.errno = BAD_METHOD
        self.error = u"PUSH method doesn't exist for page class %s" % (self.__class__.__name__,)
        return

    def put(self):
        self.errno = BAD_METHOD
        self.error = u"PUT method doesn't exist for page class %s" % (self.__class__.__name__,)
        return
    
    def delete(self):
        self.errno = BAD_METHOD
        self.error = u"DELETE method doesn't exist for page class %s" % (self.__class__.__name__,)
        return

    # These check whether the user is logged in and what permissions they have
    # before granting any access to the page. This shouldn't be overridden
    def GET(self, *args, **kwargs):
        retval = self._set_status(self.get, args, kwargs)
        return retval
    
    def PUSH(self, *args, **kwargs):
        return self._set_status(self.push, args, kwargs)
    
    def PUT(self, *args, **kwargs):
        return self._set_status(self.put, args, kwargs)
     
    def DELETE(self, *args, **kwargs):
        return self._set_status(self.delete, args, kwargs)
  
class ListPage(Page):
    permissions = 'show_list'
    table = Page.table
    priority = Page.priority
    user = Page.user
    check_vars = Page.check_vars
    permission_args = Page.permission_args
    offset = Page.offset
    limit = Page.limit
    base_link = Page.base_link
    query = Page.query
    errno = Page.errno
    error = Page.error
            
    def get_list(self):
        if self.table is None:
            self.errno = NOT_FOUND
            self.error = u"No default table set for page class %s" % (self.__class__.__name__)
            return
        if not hasattr(self.table, 'Link'):
            self.errno = NOT_FOUND
            self.error = u"Table class %s doesn't have Link attribute" % (self.table.__class__.__name__)
            return
        
        datalist = []
                
        user_data = web.input(offset=self.offset, limit=self.limit)
        try:
            user_data.limit = int(user_data.limit)
        except:
            self.errno = INVALID
            self.error = u"Unable to set limit %s for table %s" % (user_data.limit, self.table.Link)
            return
        try:
            user_data.offset = int(user_data.offset)
        except:
            self.errno = INVALID
            self.error = u"Unable to set offset %s for table %s" % (user_data.offset, self.table.Link)
            return

#        if self.query is None:
#            self.errno = 

        items = self.query.limit(user_data.limit).offset(user_data.offset)
        print items.statement
        
        for item in items:
            (index, value) = item.get_primary_key()
            datalist.append({index: value, u'link': self.gen_link(self.prefix + '/' + item.get_obj_link())})
            
        return {u'list': datalist}
    
    def _get(self):
        return self.get_list()
    
    def get(self):
        return self._get()

class ObjectPage(Page):
    permissions = 'show_object'
    table = Page.table
    priority = Page.priority
    user = Page.user
    check_vars = Page.check_vars
    permission_args = Page.permission_args
    offset = Page.offset
    limit = Page.limit
    base_link = Page.base_link
    query = Page.query
    errno = Page.errno
    error = Page.error
    
    def get_links(self, index):
        if self.table is None:
            self.errno = NOT_FOUND
            self.error = u"No default table set for page class %s" % (self.__class__.__name__)
            return
        if not hasattr(self.table, 'Link'):
            self.errno = NOT_FOUND
            self.error = u"Table class %s doesn't have Link attribute" % (self.table.__class__.__name__)
            return

        datalist = [{u'name': u'Attributes', u'link': self.gen_link(self.base_link + '/' + index + '/attributes')}]

        query = self.session.query(self.table).get(index)
        
        if query is None:
            self.errno = NOT_FOUND
            self.error = u"Unable to find primary key '%s' for table %s" % (index, self.table.Link)
            return
        
        for r in object_mapper(query).iterate_properties:
            if not isinstance(r, sqlalchemy.orm.properties.RelationshipProperty):
                continue
            
            if r.direction.name == "MANYTOONE":
                if not hasattr(r.argument.class_, "Link"):
                    continue
                
                remote = r.remote_side[0]
                test = self.session.query(remote.table).filter(remote == index).first()
                if test is None:
                    continue
                
                link = r.argument.class_.Link
                datalist.append({u'name': unicode(r.key), u'link': self.gen_link(self.base_link + '/' + index + '/' + link)})
        
        return {u'links': datalist}
    
    def _get(self, index):
        return self.get_links(index)
    
    def get(self, index):
        return self._get(index)
        
class AttrPage(Page):
    permissions = 'show_attributes'
    table = Page.table
    priority = Page.priority
    user = Page.user
    check_vars = Page.check_vars
    permission_args = Page.permission_args
    offset = Page.offset
    limit = Page.limit
    base_link = Page.base_link
    query = Page.query
    errno = Page.errno
    error = Page.error
    
    def get_attributes(self, index):
        if self.table is None:
            self.errno = NOT_FOUND
            self.error = u"No default table set for page class %s" % (self.__class__.__name__)
            return
        
        if not hasattr(self.table, 'Link'):
            self.errno = NOT_FOUND
            self.error = u"Table class %s doesn't have Link attribute" % (self.table.__class__.__name__)
            return
        
        if self.prefix != "":
            self.errno = INVALID
            self.error = u"Filters aren't allowed when getting attributes"
            return
        
        datalist = []
        
        query = self.query.get(index)
        
        for r in query.__mapper__.iterate_properties:
            key = getattr(query, r.key)
            if isinstance(r, sqlalchemy.orm.properties.RelationshipProperty):
                if key is None or _is_listish(key):
                    continue
                if key.get_obj_link() is not None:
                    datalist.append({u'name': unicode(r.key), u'value': self.gen_link(key.get_obj_link())})
                else:
                    datalist.append({u'name': unicode(r.key), u'value': None})
            else:
                datalist.append({u'name': unicode(r.key), u'value': key})
        
        if len(datalist) == 0:
            self.errno = NOT_FOUND
            self.error = u"Item %s has no attributes" % (index)
            return
        
        return {u'attributes': datalist}
    
    def _get(self, index):
        return self.get_attributes(index)
    
    def get(self, index):
        return self._get(index)

class ServerError(Page):
    error_msg = None

    def get(self):
        self.errno = INTERNAL_ERROR
        self.error = self.error_msg
        return

class Redirect(Page):
    url = '/(.*)/'
    priority = 0
    url_absolute = True
    
    def GET(self, path):
        web.seeother('/' + path)
    
def __version_check(module):
    """
    Check whether all module versions match versions in database.  If they
    don't, only show error page
    """
    for version_class in module.__subclasses__(): #@UndefinedVariable
        if len(version_class.__subclasses__()) > 0:
            if not __version_check(version_class):
                return False
        else:
            (good_version, error) = version_class(_global_data.db, _global_data.script_dir).check_version()
            if not good_version:
                globals()['ServerErrorOn'] = type('ServerErrorOn', (ServerError,), {'error_msg': error})
                urls.append('/(.*)')
                urls.append('ServerErrorOn')
                return False 
    return True
  
def __generate_auto_db():
    """
    Automatically create pages from database entries
    """
    for x in model.TableTop.__subclasses__(): #@UndefinedVariable
        if hasattr(x, 'Link'):
            globals()['Auto%sListPage' % (x.__name__,)] = type('Auto%sListPage' % (x.__name__,), (ListPage,), {'table': x, 'priority': 90, 'url': '/%s' % (x.Link,), 'base_link': x.Link})
            globals()['Auto%sObjectPage' % (x.__name__,)] = type('Auto%sObjectPage' % (x.__name__,), (ObjectPage,), {'table': x, 'priority': 90, 'url': '/%s/([^/]*)' % (x.Link,), 'base_link': x.Link})
            globals()['Auto%sAttrPage' % (x.__name__,)] = type('Auto%sAttrPage' % (x.__name__,), (AttrPage,), {'table': x, 'priority': 90, 'url': '/%s/([^/]*)/attributes' % (x.Link,), 'base_link': x.Link})

__import__('view')

if __version_check(VersionCheck):
    recursive_import(os.path.join(os.path.dirname(__file__), os.path.join('view', '__init__.py')))
    
    __generate_auto_db()
        
    __urls_from_url_dict()
    
if DEBUG:
    print urls