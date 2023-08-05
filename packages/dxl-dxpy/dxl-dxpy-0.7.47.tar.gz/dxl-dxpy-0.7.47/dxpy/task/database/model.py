import json
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine

from dxpy.time.utils import now

Base = declarative_base()


class Database:
    engine = None

    @classmethod
    def create_engine(cls):
        from .config import config as c
        cls.engine = create_engine(c.path_sqllite, echo=c['echo'])

    @classmethod
    def get_or_create_engine(cls):
        if cls.engine is None:
            cls.create_engine()
        return cls.engine

    @classmethod
    def session_maker(cls):
        return sessionmaker(bind=cls.get_or_create_engine())

    @classmethod
    def create(cls):
        Base.metadata.create_all(cls.get_or_create_engine())

    @classmethod
    def clear(cls):
        sess = cls.session_maker()()
        records = sess.query(TaskDB).delete()
        sess.commit()

    @classmethod
    def session(cls):
        return cls.session_maker()()


class TaskDB(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    desc = Column(String)
    data = Column(String)
    time_create = Column(DateTime)
    time_start = Column(DateTime)
    time_end = Column(DateTime)
    state = Column(String)
    is_root = Column(Boolean)
    ttype = Column(String)
    workdir = Column(String)
    worker = Column(String)
    dependency = Column(String)

    def __init__(self, desc, data, state=None, workdir=None, worker=None, ttype=None, dependency=None, time_create=None, time_start=None, time_end=None, is_root=True):
        self.desc = desc
        self.data = data
        if time_create is None:
            time_create = now()
        self.time_create = time_create
        if state is None:
            from .config import config as c
            state = c['default_state']
        self.state = state
        self.worker = worker
        self.workdir = workdir
        self.ttype = ttype
        self.dependency = dependency
        self.is_root = is_root

    def __repr__(self):
        return '<Task {:d}>'.format(self.id)
