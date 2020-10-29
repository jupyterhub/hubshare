import os
from tornado import web

from jupyter_server.services.contents.manager import ContentsManager
from jupyter_server.services.contents.fileio import FileManagerMixin
from jupyter_server.utils import is_hidden


class HubShareManager(FileManagerMixin, ContentsManager):
    """Contents Manager"""

    def save(self, model, path=''):
        """create a directory"""
        # Directory name in model
        dir_name = model['name']
        # Build absolute path.
        base_path = self._get_os_path(path)
        os_path = os.path.join(base_path, dir_name)

        if not os.path.exists(os_path):
            with self.perm_to_403():
                os.mkdir(os_path)
        else:
            self.log.debug("Directory %r already exists", os_path)

        return model


