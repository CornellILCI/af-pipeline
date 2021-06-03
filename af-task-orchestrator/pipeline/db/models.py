from sqlalchemy import Column, Integer, String, DateTime
from pipeline.db.core import Base


class Analysis(Base):

    __tablename__ = 'analysis'

    id = Column(Integer, primary_key=True)
    request_id = Column(String)
    sha = Column(String)
    request_type = Column(String)
    time_submitted = Column(DateTime)
    status = Column(String)
    msg = Column(String)


class Job(Base):

    __tablename__ = 'job'

    id = Column(Integer, primary_key=True)
    analysis_id = Column(Integer)
    name = Column(String)
    time_start = Column(DateTime)
    time_end = Column(DateTime)
    parent_id = Column(Integer)
    status = Column(Integer)
    err_msg = Column(String)
