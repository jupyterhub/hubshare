#!/usr/bin/env python3
"""
The HubShare main application.
"""
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from datetime import datetime
import logging
import os
from urllib.parse import urlparse

from jinja2 import Environment, FileSystemLoader
from tornado.httpserver import HTTPServer
from tornado.log import app_log, access_log, gen_log
from tornado.ioloop import IOLoop
from tornado import web

from traitlets.config import Application, catch_config_error
from traitlets import (
    Bool, Dict, Integer, List, Unicode,
    default,
)

from jupyterhub.log import CoroutineLogFormatter, log_request
from jupyterhub.services.auth import HubAuth
from jupyterhub.utils import url_path_join

from . import handlers, apihandlers

ROOT = os.path.dirname(__file__)
STATIC_FILES_DIR = os.path.join(ROOT, 'static')
TEMPLATES_DIR = os.path.join(ROOT, 'templates')

class UnicodeFromEnv(Unicode):
    """A Unicode trait that gets its default value from the environment

    Use .tag(env='VARNAME') to specify the environment variable to use.
    """
    def default(self, obj=None):
        env_key = self.metadata.get('env')
        if env_key in os.environ:
            return os.environ[env_key]
        else:
            return self.default_value

class HubShare(Application):
    """The HubShare application"""
    @property
    def version(self):
        import pkg_resources
        return pkg_resources.get_distribution('hubshare').version

    description = __doc__
    config_file = Unicode('hubshare_config.py',
        help="The config file to load",
    ).tag(config=True)
    generate_config = Bool(False,
        help="Generate default config file",
    ).tag(config=True)

    base_url = UnicodeFromEnv('/services/hubshare/').tag(
        env='JUPYTERHUB_SERVICE_PREFIX',
        config=True)
    hub_api_url = UnicodeFromEnv('http://127.0.0.1:8081/hub/api/').tag(
        env='JUPYTERHUB_API_URL',
        config=True)
    hub_api_token = UnicodeFromEnv('').tag(
        env='JUPYTERHUB_API_TOKEN',
        config=True,
    )
    hub_base_url = UnicodeFromEnv('http://127.0.0.1:8000/').tag(
        env='JUPYTERHUB_BASE_URL',
        config=True,
    )

    ip = Unicode('127.0.0.1').tag(config=True)
    @default('ip')
    def _ip_default(self):
        url_s = os.environ.get('JUPYTERHUB_SERVICE_URL')
        if not url_s:
            return '127.0.0.1'
        url = urlparse(url_s)
        return url.hostname

    port = Integer(9090).tag(config=True)
    @default('port')
    def _port_default(self):
        url_s = os.environ.get('JUPYTERHUB_SERVICE_URL')
        if not url_s:
            return 9090
        url = urlparse(url_s)
        return url.port

    template_paths = List(
        help="Paths to search for jinja templates.",
    ).tag(config=True)
    @default('template_paths')
    def _template_paths_default(self):
        return [TEMPLATES_DIR]

    tornado_settings = Dict()

    _log_formatter_cls = CoroutineLogFormatter

    @default('log_level')
    def _log_level_default(self):
        return logging.INFO

    @default('log_datefmt')
    def _log_datefmt_default(self):
        """Exclude date from default date format"""
        return "%Y-%m-%d %H:%M:%S"

    @default('log_format')
    def _log_format_default(self):
        """override default log format to include time"""
        return "%(color)s[%(levelname)1.1s %(asctime)s.%(msecs).03d %(name)s %(module)s:%(lineno)d]%(end_color)s %(message)s"

    def init_logging(self):
        """Initialize logging"""
        # This prevents double log messages because tornado use a root logger that
        # self.log is a child of. The logging module dipatches log messages to a log
        # and all of its ancenstors until propagate is set to False.
        self.log.propagate = False

        _formatter = self._log_formatter_cls(
            fmt=self.log_format,
            datefmt=self.log_datefmt,
        )

        # hook up tornado 3's loggers to our app handlers
        for log in (app_log, access_log, gen_log):
            # ensure all log statements identify the application they come from
            log.name = self.log.name
        logger = logging.getLogger('tornado')
        logger.propagate = True
        logger.parent = self.log
        logger.setLevel(self.log.level)

    def init_db(self):
        """Initialize the HubShare database"""
        self.db = None

    def init_hub_auth(self):
        """Initialize hub authentication"""
        self.hub_auth = HubAuth()

    def init_tornado_settings(self):
        """Initialize tornado config"""
        jinja_options = dict(
            autoescape=True,
        )
        jinja_env = Environment(
            loader=FileSystemLoader(self.template_paths),
            **jinja_options
        )

        # if running from git directory, disable caching of require.js
        # otherwise cache based on server start time
        parent = os.path.dirname(ROOT)
        if os.path.isdir(os.path.join(parent, '.git')):
            version_hash = ''
        else:
            version_hash=datetime.now().strftime("%Y%m%d%H%M%S"),

        settings = dict(
            log_function=log_request,
            config=self.config,
            log=self.log,
            base_url=self.base_url,
            hub_auth = self.hub_auth,
            login_url=self.hub_auth.login_url,
            hub_base_url = self.hub_base_url,
            logout_url=url_path_join(self.hub_base_url, 'hub/logout'),
            static_path=STATIC_FILES_DIR,
            static_url_prefix=url_path_join(self.base_url, 'static/'),
            template_path=self.template_paths,
            jinja2_env=jinja_env,
            version_hash=version_hash,
            xsrf_cookies=True,
        )
        # allow configured settings to have priority
        settings.update(self.tornado_settings)
        self.tornado_settings = settings

    def init_handlers(self):
        """Load hubshare's tornado request handlers"""
        self.handlers = []
        for handler in handlers.default_handlers + apihandlers.default_handlers:
            for url in handler.urls:
                self.handlers.append((url_path_join(self.base_url, url), handler))
        self.handlers.append((r'.*', handlers.Template404))

    def init_tornado_application(self):
        self.tornado_application = web.Application(self.handlers, **self.tornado_settings)

    @catch_config_error
    def initialize(self, *args, **kwargs):
        super().initialize(*args, **kwargs)
        if self.generate_config or self.subapp:
            return
        self.init_db()
        self.init_hub_auth()
        self.init_tornado_settings()
        self.init_handlers()
        self.init_tornado_application()

    def start(self):
        if self.subapp:
            self.subapp.start()
            return

        if self.generate_config:
            self.write_config_file()
            return

        self.http_server = HTTPServer(self.tornado_application, xheaders=True)
        self.http_server.listen(self.port, address=self.ip)

        self.log.info("Running HubShare at http://%s:%i%s", self.ip, self.port, self.base_url)
        IOLoop.current().start()

main = HubShare.launch_instance

if __name__ == '__main__':
    main()
