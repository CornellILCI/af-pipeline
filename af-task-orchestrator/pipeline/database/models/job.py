from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime


class Job(Base):

    __tablename__ = "job"

    id = Column(Integer, primary_key=True)
    analysis_id = Column(Integer)
    name = Column(String)
    time_start = Column(DateTime(timezone=False))
    time_end = Column(DateTime(timezone=False))
    parent_id = Column(Integer)
    status = Column(Integer)
    error_message = Column(String)
