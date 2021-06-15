from pipeline import config
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine(config.AFDB_URI)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
