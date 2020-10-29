
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


class BaseHandler(HubAuthenticated, JSContentsManager):
    """A hubshare base handler"""
    @property
    def permissions_manager(self):
        return self.settings.get('permissions_manager')

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


class UsersDirectoriesHandler(BaseHandler):
    """"""
    urls = [
        r'/users/dirs',
        r'/users/{0}{1}/dirs'.format(owner_re, path_re),
    ]

    @web.authenticated
    def get(self):
        "Get a directory list."
        pass

    @web.authenticated
    def post(self):
        """Create a directory."""
        # Get model and managers
        model = self.get_json_body()
        cm = self.contents_manager
        permissions = self.permissions_manager

        # Add data to model
        user_model = self.current_user
        owner = user_model.get('name')
        model['owner'] = owner
        model['sha'] = None #
        
        # Add directory permissions to database
        model = permissions.new_dir(model=model)
        # Create directory.
        model = cm.new(model=model)
        return model


class DirectoriesHandler(BaseHandler):

    urls = [
        r'/dirs',
        r'/dirs/{0}{1}'.format(owner_re, path_re),
    ]
    
    @web.authenticated
    def get(self, owner, path):
        pass

    @web.authenticated
    def patch(self, owner, path):
        pass

    @web.authenticated
    def delete(self, owner, path):
        pass


class CollaboratorsHandler(BaseHandler):

    urls = [
        r'/dirs/{0}{1}/collaborators'.format(owner_re, path_re),
        r'/dirs/{0}{1}/collaborators/{2}'.format(owner_re, path_re, user_re),
    ]

    @web.authenticated
    def get(self, owner, path):
        pass

    @web.authenticated
    def put(self, owner, path, username):
        pass

    @web.authenticated
    def delete(self, owner, path, username):
        pass

class ContentsHandler(BaseHandler):

    urls = [r'/dirs/{0}{1}/contents'.format(owner_re, path_re)]

    @web.authenticated
    def get(self, owner, path):
        pass 

    @web.authenticated
    def put(self, owner, path, user):
        pass

    @web.authenticated
    def delete(self, owner, path, user):
        pass

class CopiesHandler(BaseHandler):
    
    urls = [r'/dirs/{0}{1}/copies'.format(owner_re, path_re)]

    @web.authenticated
    def get(self, owner, path):
        pass

    @web.authenticated
    def post(self, owner, path):
        pass


default_handlers = [
    UsersDirectoriesHandler,
    DirectoriesHandler,
    CollaboratorsHandler,
    ContentsHandler,
    CopiesHandler
]

