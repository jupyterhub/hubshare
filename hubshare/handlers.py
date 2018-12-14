
"""handlers for human-facing pages"""

import os
from tornado import web
from tornado.log import app_log
from tornado.web import RequestHandler
from jupyterhub.services.auth import HubAuthenticated
from jupyterhub.utils import url_path_join

from jupyter_server.base.handlers import path_regex as path_re
from jupyter_server.services.contents.handlers import ContentsHandler as JSContentsManager

from . import orm

# Regular expression shorthands.
def regex_group(name):
    return r'(?P<{0}>[^/]+)'.format(name)


owner_re = regex_group('owner')
user_re = regex_group('user')


class PermissionsMixin(object):
    """Permissions extension to Contents API."""
    @property
    def db(self):
        return self.settings.get('db')

    def dir_in_db(self, dir):
        pass

    def add_dir(self, path):
        """Add a directory to permissions database."""
        print('worked')
        _, name = os.path.split(path)
        directory = orm.Dir(
            name=name,
            parent=path,
            content_url=path,
        )
        self.db.add(directory)
        self.db.commit()

    def list_dirs(self):
        for row in self.db.query(orm.Dir).all():
            print(row)

def validate_model(model):
    """Validate a dir model."""
    pass


class BaseHandler(HubAuthenticated, PermissionsMixin, JSContentsManager):
    """A hubshare base handler"""
    @property
    def config(self):
        return self.settings.get('config', None)

    @property
    def base_url(self):
        return self.settings.get('base_url', '/')

    @property
    def default_url(self):
        return self.settings.get('default_url', '')

    @property
    def version_hash(self):
        return self.settings.get('version_hash', '')

    @property
    def hub_users(self):
        return self.settings['hub_users']

    @property
    def csp_report_uri(self):
        return self.settings.get(
            'csp_report_uri',
            url_path_join(self.settings.get(
            'hub_base_url', '/hub'), 'security/csp-report')
        )

    @property
    def template_namespace(self):
        user = self.get_current_user()
        return dict(
            prefix=self.base_url,
            user=user,
            static_url=self.static_url,
            version_hash=self.version_hash,
        )

    def get_template(self, name):
        """Return the jinja template object for a given name"""
        return self.settings['jinja2_env'].get_template(name)

    def render_template(self, name, **ns):
        template_ns = {}
        template_ns.update(self.template_namespace)
        template_ns.update(ns)
        template = self.get_template(name)
        return template.render(**template_ns)


class RootDirectoryHandler(BaseHandler):
    """"""
    @web.authenticated
    def get(self):
        "Get a directory list."
        print('get')
        pass


class UsersRootDirectoryHandler(BaseHandler):
    """"""
    @web.authenticated
    def get(self):
        "Get a directory list."
        self.list_dirs()

    @web.authenticated
    def post(self):
        """Create a directory."""
        model = self.get_json_body()
        self.add_dir(model['name'])

class UsersDirectoryHandler(BaseHandler):
    """"""
    @web.authenticated
    def get(self, path):
        "Get a directory list."
        print(path)
        pass

    @web.authenticated
    def post(self, path):
        """Create a directory."""
        model = self.get_json_body()



class OwnedDirectoryHandler(BaseHandler):

    @web.authenticated
    def get(self, owner, path):
        print(owner, path)
        pass

    @web.authenticated
    def patch(self, owner, path):
        print(owner, path)
        pass

    @web.authenticated
    def delete(self, owner, path):
        print(owner, path)
        pass


class CollaboratorsListHandler(BaseHandler):

    @web.authenticated
    def get(self, owner, path):
        pass

class CollaboratorsHandler(BaseHandler):

    @web.authenticated
    def put(self, owner, path, username):
        pass

    @web.authenticated
    def delete(self, owner, path, username):
        pass

class ContentsHandler(BaseHandler):

    @web.authenticated
    def get(self, owner, path):
        pass 

    @web.authenticated
    def put(self, owner, path):
        pass

    @web.authenticated
    def delete(self, owner, path):
        pass

class CopiesHandler(BaseHandler):
    
    @web.authenticated
    def get(self, owner, path):
        pass

    @web.authenticated
    def post(self, owner, path):
        pass



# The exported handlers
default_handlers = [
    # Dirs
    (r'/dirs', 
    RootDirectoryHandler),
    (r'/dirs/{0}{1}'.format(owner_re, path_re), 
    OwnedDirectoryHandler),
    (r'/dirs/{0}{1}/collaborators'.format(owner_re, path_re),
    CollaboratorsListHandler),
    (r'/dirs/{0}{1}/collaborators/{2}'.format(owner_re, path_re, user_re),
    CollaboratorsHandler),
    (r'/dirs/{0}{1}/contents'.format(owner_re, path_re),
    ContentsHandler),
    (r'/dirs/{0}{1}/copies'.format(owner_re, path_re),
    CopiesHandler),
    (r'/users/dirs', 
    UsersRootDirectoryHandler),
    (r'/users/{0}{1}/dirs'.format(owner_re, path_re),
    UsersDirectoryHandler),
]


# class Template404(BaseHandler):
#     """Render hubshare's 404 template"""

#     def prepare(self):
#         raise web.HTTPError(404)


# class RootHandler(BaseHandler):
#     """Handler for serving hubshare's human facing pages"""

#     @web.authenticated
#     def get(self):
#         self.contents_manager.list_dir()
#         html = self.render_template('index.html')
#         self.write(html)

# class NoSlashHandler(BaseHandler):
#     def get(self):
#         self.render_template('index.html')

# default_handlers.extend([
# (r'', NoSlashHandler),
# (r'/', RootHandler),
# (r'.*', Template404),
# )]
