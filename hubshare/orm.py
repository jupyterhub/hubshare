from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    create_engine, event, exc, inspect, or_, select,
    Column, Integer, ForeignKey, Unicode, Boolean,
    DateTime, Enum, Table,
)
from sqlalchemy.orm import sessionmaker

from jupyterhub.utils import hash_token


Base = declarative_base()

# dir:user many:many mapping table
readers_map = Table('readers_map', Base.metadata,
    Column('collaborator_name', ForeignKey('collaborators.name', ondelete='CASCADE'), primary_key=True),
    Column('dir_name', ForeignKey('dirs.name', ondelete='CASCADE'), primary_key=True)
)


# dir:user many:many mapping table
writers_map = Table('writers_map', Base.metadata,
    Column('collaborator_name', ForeignKey('collaborators.name', ondelete='CASCADE'), primary_key=True),
    Column('dir_name', ForeignKey('dirs.name', ondelete='CASCADE'), primary_key=True)
)

# # dir:user many:many mapping table
# admins_map = Table('admins_map', Base.metadata,
#     Column('collaborator_name', ForeignKey('collaborators.name', ondelete='CASCADE'), primary_key=True),
#     Column('dir_name', ForeignKey('dirs.name', ondelete='CASCADE'), primary_key=True)
# )


class Dir(Base):
    """Object for storing Directories in HubShare's database.
    """
    __tablename__ = 'dirs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Unicode(255))
    sha = Column(Unicode(255), unique=True)
    content_url = Column(Unicode(255))
    created_at = Column(DateTime)
    parent = Column(Unicode(255))
    
    # permissions
    admin = Column(Boolean, default=False)
    upload = Column(Boolean, default=True)
    download = Column(Boolean, default=True)

    @classmethod
    def find(cls, db, name):
        """Find a group by name.
        Returns None if not found.
        """
        return db.query(cls).filter(cls.name == name).first()

    def __repr__(self):
        return "<{cls}({name} {created_at} {admin})>".format(
            cls=self.__class__.__name__,
            name=self.name,
            created_at=self.created_at,
            admin=self.admin
        )


class Collaborators(Base):
    """Object for storing Directories in HubShare's database.
    """
    __tablename__ = 'collaborators'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Unicode(255), unique=True)
    type = Column(Unicode(255), default='user')

    @classmethod
    def find(cls, db, name):
        """Find a group by name.
        Returns None if not found.
        """
        return db.query(cls).filter(cls.name == name).first()


def new_session_factory(url="sqlite:///:memory:",
                        reset=False,
                        expire_on_commit=False,
                        **kwargs):
    """Create a new session at url"""
    engine = create_engine(url, **kwargs)
    # enable pessimistic disconnect handling
    Base.metadata.create_all(engine)

    # We set expire_on_commit=False, since we don't actually need
    # SQLAlchemy to expire objects after committing - we don't expect
    # concurrent runs of the hub talking to the same db. Turning
    # this off gives us a major performance boost
    session_factory = sessionmaker(bind=engine,
                                   expire_on_commit=expire_on_commit,
                                   )
    return session_factory
