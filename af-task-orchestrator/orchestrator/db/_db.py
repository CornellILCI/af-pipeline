"""
_db.py: contains sqlalchemy engine and session for task usage

"""

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from orchestrator.config import AFDB_URL

engine = create_engine(
    AFDB_URL, convert_unicode=True, pool_recycle=3600, pool_size=10
) # TODO: convert params to config values

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
