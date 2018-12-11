
"""handlers for human-facing pages"""

from tornado import web
from tornado.log import app_log
from tornado.web import RequestHandler
from jupyterhub.services.auth import HubAuthenticated
from jupyterhub.utils import url_path_join


class BaseHandler(HubAuthenticated, web.RequestHandler):
    """A hubshare base handler"""
    def prepare(self):
        super().prepare()
        self.contents_manager.request = self.request

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

    # The next two methods exist to circumvent the basehandler's async
    # versions of the methods.
    @property
    def contents_manager(self):
        return self.settings['contents_manager']

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


class Template404(BaseHandler):
    """Render hubshare's 404 template"""

    def prepare(self):
        raise web.HTTPError(404)


class RootHandler(BaseHandler):
    """Handler for serving hubshare's human facing pages"""

    @web.authenticated
    def get(self):
        self.contents_manager.list_dir()
        html = self.render_template('index.html')
        self.write(html)

class NoSlashHandler(BaseHandler):
    def get(self):
        self.render_template('index.html')

# The exported handlers
default_handlers = [
    (r'', NoSlashHandler),
    (r'/', RootHandler),
    (r'.*', Template404)
]
