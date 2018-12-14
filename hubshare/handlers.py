
"""handlers for human-facing pages"""

from tornado import web
from tornado.log import app_log
from tornado.web import RequestHandler
from jupyterhub.services.auth import HubAuthenticated
from jupyterhub.utils import url_path_join

from jupyter_server.base.handlers import path_regex
from . import orm


user_regex = r'/(?P<user>[^/]+){0}'.format(path_regex)
owner_regex = r'/(?P<owner>[^/]+){0}'.format(path_regex)


class PermissionsMixin(object):
    """Permissions extension to Contents API."""
    @property
    def db(self):
        return self.settings.get('db')


class BaseHandler(HubAuthenticated, PermissionsMixin, RequestHandler):
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

    def finish(self):
        return super(BaseHandler, self).finish()


class UsersDirectoryHandler(BaseHandler):
    """"""
    @web.authenticated
    def get(self, path=''):
        "Get a directory list."
        pass

    @web.authenticated
    def post(self, path=''):
        """Create a directory."""
        pass


class OwnedDirectoryHandler(BaseHandler):

    @web.authenticated
    def get(self, owner, path):
        print(owner, path)
        pass

    @web.authenticated
    def patch(self, owner, path):
        pass

    @web.authenticated
    def delete(self, owner, path):
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
    (r'/dirs', UsersDirectoryHandler),
    (r'/dirs/(?P<owner>[^/]+){0}'.format(path_regex), OwnedDirectoryHandler),
    (r'/dirs/(?P<owner>[^/]+){0}/collaborators'.format(path_regex), CollaboratorsListHandler),
    (r'/dirs/(?P<owner>[^/]+){0}/collaborators/(?P<username>[^/]+)'.format(path_regex),
     CollaboratorsListHandler),
    (r'/dirs/(?P<owner>[^/]+){0}/contents'.format(path_regex), ContentsHandler),
    (r'/dirs/(?P<owner>[^/]+){0}/copies'.format(path_regex), CopiesHandler),
    (r'/users/dirs', UsersDirectoryHandler),
    (r'/users/(?P<user>[^/]+){0}/dirs'.format(path_regex), UsersDirectoryHandler),

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
