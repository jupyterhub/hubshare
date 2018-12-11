from tornado.wsgi import WSGIContainer
from .base import ContentsManager

from tempfile import gettempdir

from wsgidav.wsgidav_app import WsgiDAVApp
from wsgidav.fs_dav_provider import FilesystemProvider
from wsgidav.default_conf import DEFAULT_CONFIG as config

from wsgidav.debug_filter import WsgiDavDebugFilter
from wsgidav.dir_browser import WsgiDavDirBrowser
from wsgidav.error_printer import ErrorPrinter
from wsgidav.http_authenticator import HTTPAuthenticator
from wsgidav.request_resolver import RequestResolver

from tornado.httputil import HTTPServerRequest, HTTPHeaders
from jupyterhub.utils import url_path_join


class WebDavManager(ContentsManager):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Testing with root provider
        provider = FilesystemProvider(self.root_dir)

        config["provider_mapping"] = {"/": provider}
        config["middleware_stack"] = [
            WsgiDavDebugFilter,
            ErrorPrinter,
            HTTPAuthenticator,
            RequestResolver,
        ]
        config["http_authenticator"] = {
            "accept_basic": True,  # Allow basic authentication, True or False
            "accept_digest": False,  # Allow digest authentication, True or False
        }

        # Add WebDAV specific config to traits config.
        self.config.update(config)

        # Create a WSGI Application and wrap in tornado container
        self.wsgi_app = WSGIContainer(WsgiDAVApp(self.config))
        # Add handlers?

    @property
    def request(self):
        return self._request

    @request.setter
    def request(self, request):
        self._request = request
        
    def list_dir(self, path="/"):
        request = HTTPServerRequest(
            "PROPFIND",
            uri=path,
            # version="HTTP/1.1",
            # headers=headers
            connection=self.request.connection
        )
        response = self.wsgi_app(self.request)
        print(self.request.headers)
        print(self.request.body)
        print("Hello, world")
