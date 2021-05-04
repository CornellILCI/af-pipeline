
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from pipeline.config import get_database_url


engine = create_engine(get_database_url())

SessionLocal = sessionmaker(bind=engine)
