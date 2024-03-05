# """
# _db.py: contains sqlalchemy engine and session for task usage

# """

# # deprecate in favor of the af.pipeline db config
# from af.orchestrator.config import AFDB_URL
# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker

# db_engine = create_engine(
#     AFDB_URL, convert_unicode=True, pool_recycle=3600, pool_size=10
# )  # TODO: convert params to config values

# db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=db_engine))
