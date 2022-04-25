import json

from database import Property, PropertyConfig, PropertyMeta, db
from sqlalchemy import and_, func

from af_config import api_models
from af_config import models as db_models
from database import db


def get_analysis_configs(page=0, page_size=1000, **kwargs):

    query_params = {}

    # make sure to add only non null query params
    query_params = {k: [v] for k, v in kwargs.items() if v is not None}

    analysis_config_base_property = Property.query.filter(Property.code == "analysis_config").one()

    # sub query to aggregate metadata code and value
    analysis_configs_sub_q = (
        db.session.query(Property.id, PropertyMeta.code, func.array_agg(PropertyMeta.value).label("meta_value"))
        .select_from(PropertyConfig)
        .join(
            Property,
            and_(
                Property.id == PropertyConfig.config_property_id,
                Property.id != analysis_config_base_property.id,
                PropertyConfig.property_id == analysis_config_base_property.id,
            ),
        )
        .join(PropertyMeta, Property.id == PropertyMeta.property_id)
        .group_by(Property.id, PropertyMeta.code)
        .subquery()
    )

    # query aggregated metadata code and value as json object
    analysis_configs_q = (
        db.session.query(Property)
        .select_from(analysis_configs_sub_q)
        .group_by(analysis_configs_sub_q.c.id, Property)
        .having(
            func.jsonb_object_agg(analysis_configs_sub_q.c.code, analysis_configs_sub_q.c.meta_value).op("@>")(
                json.dumps(query_params)
            )
        )
        .join(Property, Property.id == analysis_configs_sub_q.c.id)
        .order_by(Property.id)
    )

    total_count = analysis_configs_q.count()

    if page_size is not None:
        analysis_configs_q = analysis_configs_q.limit(page_size)

    if page is not None:
        analysis_configs_q = analysis_configs_q.offset(page * page_size)

    analysis_configs = analysis_configs_q.all()

    return analysis_configs, total_count


def submit_analysis_config(request_params: api_models.Analysis,
                           request_params_meta: api_models.AnalysisConfigMeta,
                           request_params_config: api_models.ParamsConfig):

    """Submits analysis config to pipeline."""

    analysis_uuid = str(uuidlib.uuid4())

    analysis_property = Property(
        # (code, "name", "label", description, "type", data_type, creator_id, is_void, tenant_id, id, "statement")
        code=request_params.code,
        name=request_params.configName,
        label=request_params.label,
        description=request_params.description,
        type=request_params.design,
        data_type=request_params.dataType,
        creator_id=request_params.creator_id,
        modifier_id=request_params.modifier_id,
        is_void=request_params.isVoid,
        tenant_id=request_params.tenantId,
        id=request_params.id,
        statement=request_params.statement
    )

    analysis_config_meta = PropertyMeta(
        # property_id, code, value, tenant_id
        property_id=request_params_meta.property_id,
        code=request_params_meta.code,
        value= request_params_meta.value,
        tenant_id =request_params_meta.tenant_id

    )

    analysis_config = PropertyConfig(
        order_number=request_params_config.order,
        creator_id=request_params_config.creator_id,
        is_void=request_params_config.is_void,
        property_id=request_params_config.property_id,
        config_property_id=request_params_config.config_property_id,
        is_layout_variable=request_params_config.is_layout_variable,

    )


    with db.session.begin():
        # i may need to add multiple analysis config metas,
        db.session.add(analysis_property)
        db.session.add(analysis_config_meta)
        db.session.add(analysis_config)

        celery_util.send_task(
            process_name="analyze",
            args=(
                req.uuid,
                json.loads(request_params.json()),
            ),
        )

    return analysis

# https://bitbucket.org/ebsproject/ba-db/src/develop/build/liquibase/changesets/21.09/data/template/add_2_new_models_for_cimmyt.sql?atlOrigin=eyJpIjoiMWRiZjlmZjhkYmE3NDg0Mzk3NWI3ODZhZjczNGQyODQiLCJwIjoiYmItY2hhdHMtaW50ZWdyYXRpb24ifQ