from af.tests import setup  # noqa:F401 isort:skip
import tempfile

import pytest
from af.pipeline import db
from af.pipeline import config
from af.tests.fixtures.sample_asremlr_1 import sample_asreml_result_string_1  # noqa: F401
from af.tests.fixtures.sample_asremlr_2 import sample_asreml_not_converged_result_string  # noqa: F401
from af.tests.fixtures.sample_brapi_observation_table_response import (  # noqa: F401
    brapi_observation_table_api_response_1,
)
from af.tests.fixtures.sample_yhat_1 import sample_yhat_data_1  # noqa: F401
from sqlalchemy.engine.create import create_engine
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.session import Session, sessionmaker  # noqa: F401

from af.tests import common

from pgtest.pgtest import PGTest
from sqlalchemy import create_engine


pg = PGTest()


@pytest.fixture(scope="function")
def temp_dir():
    return tempfile.TemporaryDirectory()


@pytest.fixture(scope="session")
def engine():
    return create_engine(pg.url)


@pytest.fixture(scope="session")
def tables(engine):
    engine.execute("CREATE SCHEMA af")
    db.core.Base.metadata.create_all(engine)
    yield
    db.core.Base.metadata.drop_all(engine)


@pytest.fixture(autouse=True)
def dbsession(engine, tables):

    """Returns an sqlalchemy session, and after the test tears down everything properly."""
    connection = engine.connect()
    # begin the nested transaction
    transaction = connection.begin()
    # use the connection with the already started transaction
    session = scoped_session(sessionmaker(bind=connection))

    yield session

    session.close()
    # roll back the broader transaction
    transaction.rollback()
    # put back the connection to the connection pool
    connection.close()
