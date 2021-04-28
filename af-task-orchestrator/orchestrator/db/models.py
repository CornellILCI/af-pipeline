"""models.py"""
from orchestrator.db import db_engine
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()
Base.metadata.schema = "af"
Base.metadata.reflect(db_engine)


class Request(Base):
    __table__ = Base.metadata.tables["af.request"]

    # TODO add the other columns here
    tasks = relationship("Task", backref="request", foreign_keys="Task.request_id")


class Task(Base):
    __table__ = Base.metadata.tables["af.task"]
