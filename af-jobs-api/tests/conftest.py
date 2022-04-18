import tempfile

import pytest
from af_endpoints import af_apis
from af_request.models import Request
from af_request.views import af_requests_bp
from pgtest.pgtest import PGTest

from api import create_app

from . import factories as model_factory
from .factories import (
    AnalysisFactory,
    AnalysisRequestParametersFacotry,
    BaseFactory,
    JobFactory,
    PropertyFactory,
    RequestFactory,
)
from .factories import db as _db

pg = PGTest()

settings_override = {
    "SQLALCHEMY_DATABASE_URI": pg.url,
    "SQLALCHEMY_TRACK_MODIFICATIONS": False,
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
    _db.engine.execute("CREATE SCHEMA af")
    _db.create_all()

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(autouse=True, scope="function")
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
        db.session.remove()

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
def empty_request():
    return {}


@pytest.fixture
def incorrect_request():
    return {"foo": "bar"}


@pytest.fixture
def incorrect_request_2():
    return {
        "dataSource": "NOT_EBS",
        "dataSourceUrl": "foo",
        "dataSourceAccessToken": "test-token",
        "crop": "rice",
        "institute": "IRRI",
        "analysisType": "ANALYZE",
        "experiments": [],
        "occurrences": [],
        "traits": [],
        "analysisObjectivePropertyId": None,
        "analysisConfigPropertyId": None,
        "expLocAnalysisPatternPropertyId": None,
        "configFormulaPropertyId": None,
        "configResidualPropertyId": None,
    }


@pytest.fixture
def correct_request(session):

    return {
        "dataSource": "EBS",
        "dataSourceUrl": "foo",
        "dataSourceAccessToken": "test-token",
        "crop": "rice",
        "institute": "IRRI",
        "analysisType": "ANALYZE",
        "experiments": [{"experimentId": "10", "experimentName": "expt1"}],
        "occurrences": [{"occurrenceId": "10", "occurrenceName": "occur1"}],
        "traits": [{"traitId": "1", "traitName": "trait1"}, {"traitId": "2", "traitName": "trait2"}],
        "analysisObjectivePropertyId": "1",
        "analysisConfigPropertyId": "2",
        "expLocAnalysisPatternPropertyId": "3",
        "configFormulaPropertyId": "4",
        "configResidualPropertyId": "5",
    }


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

    analyses = AnalysisFactory.create_batch(size=2)
    session.commit()
    return analyses


@pytest.fixture
def af_request_parameters(session):

    PropertyFactory._meta.sqlalchemy_session = session

    analysis_request_parameters = AnalysisRequestParametersFacotry(
        analysisObjectivePropertyId=PropertyFactory().id,
        analysisConfigPropertyId=PropertyFactory().id,
        expLocAnalysisPatternPropertyId=PropertyFactory().id,
        configFormulaPropertyId=PropertyFactory().id,
        configResidualPropertyId=PropertyFactory().id,
    )
    session.commit()
    return analysis_request_parameters


@pytest.fixture
def random_properties(session):

    properties = model_factory.RandomPropertyFactory.create_batch(size=10)

    return properties


@pytest.fixture
def analysis_configs(session):

    model_factory.PropertyFactory._meta.sqlalchemy_session = session

    base_analysis_config = model_factory.AnalysisConfigsRootFactory()

    analysis_configs = []
    for property_config in base_analysis_config.property_configs:
        if property_config.property_id != property_config.config_property_id:
            analysis_configs.append(property_config.property_config_property)
    return analysis_configs


@pytest.fixture
def analysis_configs_unordered(session):

    model_factory.PropertyFactory._meta.sqlalchemy_session = session

    base_analysis_config = model_factory.AnalysisConfigsRootUnorderedFactory()

    analysis_configs = []
    for property_config in base_analysis_config.property_configs:
        if property_config.property_id != property_config.config_property_id:
            analysis_configs.append(property_config.property_config_property)
    return analysis_configs


@pytest.fixture
def analysis_configs_with_design_metadata(session):

    model_factory.PropertyFactory._meta.sqlalchemy_session = session

    base_analysis_config = model_factory.AnalysisConfigsRootFactory()

    # add configs with design
    design_metadata_property_configs = model_factory.AnalysisConfigsWithDesignPropertyConfigFactory.create_batch(
        size=10, property_id=base_analysis_config.id
    )

    base_analysis_config.property_configs.extend(design_metadata_property_configs)

    session.commit()

    analysis_configs = []
    for property_config in design_metadata_property_configs:
        if property_config.property_id != property_config.config_property_id:
            analysis_configs.append(property_config.property_config_property)

    return analysis_configs


@pytest.fixture
def analysis_configs_with_engine_metadata(session):

    model_factory.PropertyFactory._meta.sqlalchemy_session = session

    base_analysis_config = model_factory.AnalysisConfigsRootFactory()

    # add configs with engine
    engine_metadata_property_configs = model_factory.AnalysisConfigsWithEnginePropertyConfigFactory.create_batch(
        size=10, property_id=base_analysis_config.id
    )

    base_analysis_config.property_configs.extend(engine_metadata_property_configs)

    session.commit()

    analysis_configs = []
    for property_config in engine_metadata_property_configs:
        if property_config.property_id != property_config.config_property_id:
            analysis_configs.append(property_config.property_config_property)

    return analysis_configs


@pytest.fixture
def analysis_configs_with_trait_level_metadata(session):

    model_factory.PropertyFactory._meta.sqlalchemy_session = session

    base_analysis_config = model_factory.AnalysisConfigsRootFactory()

    # add configs with trait level
    trait_level_metadata_property_configs = (
        model_factory.AnalysisConfigsWithTraitLevelPropertyConfigFactory.create_batch(
            size=10, property_id=base_analysis_config.id
        )
    )

    base_analysis_config.property_configs.extend(trait_level_metadata_property_configs)

    session.commit()

    analysis_configs = []
    for property_config in trait_level_metadata_property_configs:
        if property_config.property_id != property_config.config_property_id:
            analysis_configs.append(property_config.property_config_property)

    return analysis_configs


@pytest.fixture
def analysis_configs_with_analysis_objective_metadata(session):

    model_factory.PropertyFactory._meta.sqlalchemy_session = session

    base_analysis_config = model_factory.AnalysisConfigsRootFactory()

    # add configs with objective
    objective_metadata_property_configs = (
        model_factory.AnalysisConfigsWithAnalysisObjectivePropertyConfigFactory.create_batch(
            size=10, property_id=base_analysis_config.id
        )
    )

    base_analysis_config.property_configs.extend(objective_metadata_property_configs)

    session.commit()

    analysis_configs = []
    for property_config in objective_metadata_property_configs:
        if property_config.property_id != property_config.config_property_id:
            analysis_configs.append(property_config.property_config_property)

    return analysis_configs


@pytest.fixture
def analysis_configs_with_exp_pattern_metadata(session):

    model_factory.PropertyFactory._meta.sqlalchemy_session = session

    base_analysis_config = model_factory.AnalysisConfigsRootFactory()

    # add configs with exp pattern
    exp_pattern_metadata_property_configs = (
        model_factory.AnalysisConfigsWithExpPatternPropertyConfigFactory.create_batch(
            size=10, property_id=base_analysis_config.id
        )
    )

    base_analysis_config.property_configs.extend(exp_pattern_metadata_property_configs)

    session.commit()

    analysis_configs = []
    for property_config in exp_pattern_metadata_property_configs:
        if property_config.property_id != property_config.config_property_id:
            analysis_configs.append(property_config.property_config_property)

    return analysis_configs
