"""Handlers for the REST API"""
from tornado import web
from .handlers import BaseHandler, path_re

class APIHandler(BaseHandler):
    
    urls = [r'/api/{0}'.format(path_re)]

    @web.authenticated
    def get(self, name):
        pass



default_handlers = [
    APIHandler
]
