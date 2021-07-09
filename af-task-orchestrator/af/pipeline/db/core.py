from af.pipeline import config
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker


class DBConfig:
    _engine = None

    @classmethod
    def get_engine(cls):
        if DBConfig._engine:
            return DBConfig._engine
        DBConfig._engine = create_engine(config.AFDB_URI)
        return DBConfig._engine

    _SessionLocal = None

    def get_session():
        if DBConfig._SessionLocal:
            return DBConfig._SessionLocal
        DBConfig._SessionLocal = scoped_session(sessionmaker(DBConfig.get_engine()))
        print(DBConfig._SessionLocal, "n")
        return DBConfig._SessionLocal


Base = declarative_base()
