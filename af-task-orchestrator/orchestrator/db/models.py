"""models.py"""
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class Request(Base):
    __tablename__ = 'request'


class Task(Base):
    __tablename__ = 'task'





 