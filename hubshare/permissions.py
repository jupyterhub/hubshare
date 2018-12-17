"""Class for managing local filesystem permissions."""
import os
from traitlets.config import LoggingConfigurable

from . import orm

class PermissionsManager(LoggingConfigurable):
    """Class for managing permissions of content on local
    file system.
    """

    def __init__(self, db, **traits):
        super().__init__(**traits)
        self.db = db

    def new_dir(self, path):
        """Add a directory to permissions database."""
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
            pass
