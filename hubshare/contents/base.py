from traitlets.config import Configurable
from traitlets import (
    Unicode
)

class NotImplementedError(Exception):
    """"""


class ContentsManager(Configurable):
    """Base class of all contents managers provided by Hubshare.
    """

    root_dir = Unicode(
        "/Users/zsailer/Documents/calpoly/projects/hubshare/hubshare/examples/test",
        help="""
        Root path where the shared content lives.
        """,
        config=True
    )

    def _base_model(self):
        pass

    def _dir_model(self, path=''):
        pass

    def _collaborators_model(self):
        pass

    def dir_exists(self, path):
        """Does a directory exist at the given path?

        Like os.path.isdir

        Override this method in subclasses.

        Parameters
        ----------
        path : string
            The path to check

        Returns
        -------
        exists : bool
            Whether the path does indeed exist.
        """
        raise NotImplementedError

    def is_hidden(self, path):
        """Is path a hidden directory or file?

        Parameters
        ----------
        path : string
            The path to check. This is an API path (`/` separated,
            relative to root dir).

        Returns
        -------
        hidden : bool
            Whether the path is hidden.

        """
        raise NotImplementedError

    def file_exists(self, path=''):
        """Does a file exist at the given path?

        Like os.path.isfile

        Override this method in subclasses.

        Parameters
        ----------
        path : string
            The API path of a file to check for.

        Returns
        -------
        exists : bool
            Whether the file exists.
        """
        raise NotImplementedError('must be implemented in a subclass')

    def exists(self, path):
        """Does a file or directory exist at the given path?

        Like os.path.exists

        Parameters
        ----------
        path : string
            The API path of a file or directory to check for.

        Returns
        -------
        exists : bool
            Whether the target exists.
        """
        return self.file_exists(path) or self.dir_exists(path)

    def get(self, path, content=True, type=None, format=None):
        """Get a file or directory model."""
        raise NotImplementedError('must be implemented in a subclass')

    def save(self, model, path):
        """
        Save a file or directory model to path.

        Should return the saved model with no content.  Save implementations
        should call self.run_pre_save_hook(model=model, path=path) prior to
        writing any data.
        """
        raise NotImplementedError('must be implemented in a subclass')

    def delete_file(self, path):
        """Delete the file or directory at path."""
        raise NotImplementedError('must be implemented in a subclass')

    def rename_file(self, old_path, new_path):
        """Rename a file or directory."""
        raise NotImplementedError('must be implemented in a subclass')
