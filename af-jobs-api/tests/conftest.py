import tempfile

import pytest
from af_endpoints import af_apis
from af_request.models import Request
from af_request.views import af_requests_bp

from api import create_app

from .factories import (
    AnalysisFactory,
    AnalysisRequestParametersFacotry,
    BaseFactory,
    JobFactory,
    PropertyFactory,
    RequestFactory,
)
from .factories import db as _db

TEST_DATABASE_URI = "sqlite://"

settings_override = {
    "TESTING": True,
    "SQLALCHEMY_DATABASE_URI": TEST_DATABASE_URI,
}


@pytest.fixture
def temp_dir():

    import tempfile
    fp = tempfile.NamedTemporaryFile()


@pytest.fixture(scope="session")
def app(request):
    """Test flask app"""

    # mock the celery_app

    app = create_app(settings_override)
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope="session")
def db(app, request):
    """session db"""

    def teardown():
        _db.drop_all()

    _db.init_app(app)
    _db.engine.execute("ATTACH DATABASE ':memory:' AS af")
    _db.create_all()

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope="function")
def session(db, request):

    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)
    db.session = session

    # Set sessions for request factories
    # For some reason using common session not working

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return db.session


@pytest.fixture(scope="function")
def celery_send_task(mocker):
    mock = mocker.MagicMock()
    mocker.patch("celery_util.send_task", mock)
    return mock


@pytest.fixture(scope="function")
def client(session, app, db):
    with app.test_client() as client:
        yield client


@pytest.fixture
def analysis(session):

    AnalysisFactory._meta.sqlalchemy_session = session
    RequestFactory._meta.sqlalchemy_session = session
    PropertyFactory._meta.sqlalchemy_session = session
    JobFactory._meta.sqlalchemy_session = session

    analysis = AnalysisFactory()
    return analysis


@pytest.fixture
def analyses(session):

    AnalysisFactory._meta.sqlalchemy_session = session
    RequestFactory._meta.sqlalchemy_session = session
    PropertyFactory._meta.sqlalchemy_session = session
    JobFactory._meta.sqlalchemy_session = session

    analyses = [AnalysisFactory(), AnalysisFactory()]

    return analyses


@pytest.fixture
def af_request_parameters():
    analysis_request_parameters = AnalysisRequestParametersFacotry()
    return analysis_request_parameters
