import pytest
import tempfile
from api import create_app
from database import db as _db
from database import Request
from af_requests_endpoints import af_requests_bp

TESTDB = 'af.db'
TEST_DB_PATH = tempfile.gettempdir() + f"/{TESTDB}"
print(TEST_DB_PATH)
TEST_DATABASE_URI = 'sqlite:///' + TEST_DB_PATH  # in memory db

settings_override = {
    'TESTING': True,
    'SQLALCHEMY_DATABASE_URI': TEST_DATABASE_URI,
    'SQLALCHEMY_BINDS': {
        'af': TEST_DATABASE_URI
    }
}

@pytest.fixture(scope='session')
def app(request):
    """Test flask app"""
    app = create_app(settings_override)
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app

@pytest.fixture(scope='session')
def db(app, request):
    """session db"""
    import os
    if os.path.exists(TEST_DB_PATH):
        os.unlink(TEST_DB_PATH)

    def teardown():
        _db.drop_all()
        os.unlink(TEST_DB_PATH)

    _db.init_app(app)
    _db.create_all(bind=['af'])

    request.addfinalizer(teardown)
    return _db

@pytest.fixture(scope='function')
def session(db, request):

    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={'af': TEST_DATABASE_URI})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def client(session, app):
    with app.test_client() as client:
        yield client
