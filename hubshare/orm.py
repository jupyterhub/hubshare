from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    create_engine, event, exc, inspect, or_, select,
    Column, Integer, ForeignKey, Unicode, Boolean,
    DateTime, Enum, Table,
)

from jupyterhub.utils import hash_token
from jupyterhub.orm import (
    new_session_factory,

)

Base = declarative_base()

# dir:user many:many mapping table
readers_map = Table('readers_map', Base.metadata,
    Column('collaborator_name', ForeignKey('collaborators.name', ondelete='CASCADE'), primary_key=True),
    Column('dir_name', ForeignKey('dirs.name', ondelete='CASCADE'), primary_key=True)
)


# dir:user many:many mapping table
writers_map = Table('readers_map', Base.metadata,
    Column('collaborator_name', ForeignKey('collaborators.name', ondelete='CASCADE'), primary_key=True),
    Column('dir_name', ForeignKey('dirs.name', ondelete='CASCADE'), primary_key=True)
)

# dir:user many:many mapping table
admins_map = Table('readers_map', Base.metadata,
    Column('collaborator_name', ForeignKey('collaborators.name', ondelete='CASCADE'), primary_key=True),
    Column('dir_name', ForeignKey('dirs.name', ondelete='CASCADE'), primary_key=True)
)


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

    # def __repr__(self):
    #     return "{cls}({name})".format(
    #         cls=self.__class__, 
    #         name=self.name
    #     )


class Collaborators(Base):
    """Object for storing Directories in HubShare's database.
    """
    __tablename__ = 'collaborators'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Unicode(255), unique=True)
    type = Column(Unicode(255), default='user')
