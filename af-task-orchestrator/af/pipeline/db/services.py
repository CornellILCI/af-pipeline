from datetime import datetime

from af.pipeline.db.models import Analysis, Job, Property, PropertyConfig, PropertyMeta, Request
from sqlalchemy import and_, func
from sqlalchemy.orm import aliased

# TODO: Catch database exceptions, mainly NoResultFounException


def get_property(db_session, property_id: str) -> Property:
    return db_session.query(Property).get(property_id)


def get_child_properties(db_session, property_root: str, property_name: str) -> list[Property]:
    child_property_root = db_session.query(Property).filter(Property.code == property_code).one()
    properties = (
        db_session.query(Property)
        .select_from(PropertyConfig)
        .join(
            Property,
            and_(
                Property.id == PropertyConfig.config_property_id,
                Property.id != child_property_root.id,
                PropertyConfig.property_id == child_property_root.id,
            ),
        )
        .all()
    )

    return properties


def get_request(db_session, request_id) -> Request:
    return db_session.query(Request).filter(Request.uuid == request_id).one()


def get_analysis_by_request_id(db_session, request_id):
    return db_session.query(Analysis).join(Request).filter(Request.uuid == request_id).first()


def get_job_by_name(db_session, job_name) -> Job:
    return db_session.query(Job).filter(Job.name == job_name).one()


def create_job(db_session, analysis_id: int, job_name: str, status: str, status_message: str) -> Job:

    job_start_time = datetime.utcnow()
    job = Job(
        analysis_id=analysis_id,
        name=job_name,
        time_start=job_start_time,
        creation_timestamp=job_start_time,
        status=status,
        status_message=status_message,
    )

    job = add(db_session, job)

    return job


def update_job(db_session, job: Job, status: str, status_message: str):

    job.status = status
    job.status_message = status_message
    job.time_end = datetime.utcnow()
    job.modification_timestamp = datetime.utcnow()

    return job


def get_analysis_config_properties(db_session, analysis_config_id: str, property_code: str) -> list[Property]:

    _analysis_config_property_configs = aliased(PropertyConfig)

    child_property_root = db_session.query(Property).filter(Property.code == property_code).one()

    properties = (
        db_session.query(Property)
        .select_from(PropertyConfig)
        .join(
            _analysis_config_property_configs,
            and_(
                PropertyConfig.property_id == child_property_root.id,
                PropertyConfig.config_property_id == _analysis_config_property_configs.config_property_id,
                _analysis_config_property_configs.property_id == analysis_config_id,
            ),
        )
        .join(Property, Property.id == PropertyConfig.config_property_id)
        .all()
    )

    return properties


def get_analysis_config_meta_data(db_session, analysis_config_id: str, meta_code: str) -> PropertyMeta:

    _property = (
        db_session.query(PropertyMeta)
        .join(
            Property,
            and_(
                Property.id == PropertyMeta.property_id,
                Property.id == analysis_config_id,
                PropertyMeta.code == meta_code,
            ),
        )
        .one()
    )
    return _property


def get_analysis_config_module_fields(db_session, analysis_config_id: str):
    """Gets Analysis module fields for give analysis config id.

    Args:
        analysis_config_id: Id fo the analysis configuration

    Returns:
        (Property, property_meta)
            Property - Property of analysis field
            property_meta - Json
    """

    _analysis_config_property_configs = aliased(PropertyConfig)

    analysis_field_root = db_session.query(Property).filter(Property.code == "analysis_module_fields").one()

    _property_meta = func.jsonb_object_agg(PropertyMeta.code, PropertyMeta.value).label("property_meta")

    module_fields = (
        db_session.query(Property, _property_meta)
        .select_from(PropertyConfig)
        .join(
            _analysis_config_property_configs,
            and_(
                PropertyConfig.property_id == analysis_field_root.id,
                PropertyConfig.config_property_id == _analysis_config_property_configs.config_property_id,
                _analysis_config_property_configs.property_id == analysis_config_id,
            ),
        )
        .join(Property, Property.id == PropertyConfig.config_property_id)
        .join(PropertyMeta, Property.id == PropertyMeta.property_id)
        .group_by(Property.id)
        .all()
    )

    return module_fields


def add(db_session, _object):
    db_session.add(_object)
    db_session.commit()
    return _object
