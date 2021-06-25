from af.pipeline import config
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session

engine = create_engine(config.AFDB_URI)

SessionLocal = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()


def get_session():
    """Impl: DI friendly"""
    print("This is called")
    global SessionLocal
    return SessionLocal
