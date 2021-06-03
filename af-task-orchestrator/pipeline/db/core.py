from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from pipeline import config

engine = create_engine(config.AFDB_URI)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
