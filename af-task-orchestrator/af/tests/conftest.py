from af.tests import setup  # noqa:F401 isort:skip

import pytest
from af.pipeline import config
from af.pipeline.db.core import Base
from af.tests.fixtures.sample_asremlr_1 import sample_asreml_result_string_1  # noqa: F401
from sqlalchemy.engine.create import create_engine
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.session import Session, sessionmaker


@pytest.fixture(scope="session")
def engine():
    engine = create_engine(config.get_afdb_uri())
    engine.execute("ATTACH DATABASE ':memory:' AS af")
    return engine


@pytest.fixture(scope="session")
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def dbsession(engine, tables):
    connection = engine.connect()
    transaction = connection.begin()
    session = scoped_session(sessionmaker(bind=connection))
    yield session
    transaction.rollback()
    connection.close()
