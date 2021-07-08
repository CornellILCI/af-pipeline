import tempfile

import pytest
from af_endpoints import af_apis
from af_request.models import Request
from af_request.views import af_requests_bp
from database import db as _db

from api import create_app

from .factories import RequestFactory


TEST_DATABASE_URI = "sqlite://"

settings_override = {
    "TESTING": True,
    "SQLALCHEMY_DATABASE_URI": TEST_DATABASE_URI,
}


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
    
    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return db.session


@pytest.fixture(scope="function")
def client(session, app, db):
    with app.test_client() as client:
        yield client


@pytest.fixture
def af_request(session):
    request = RequestFactory()
    return request


@pytest.fixture
def af_requests(session):
    request = RequestFactory()
    session.add(request)
    session.commit()
    return [request]
