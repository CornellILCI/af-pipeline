import json

from database import Property, PropertyConfig, PropertyMeta, db
from sqlalchemy import and_, func

from analysis_config import api_models
from analysis_config import models as db_models
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
                           request_params_config: api_models.AnalysisConfig):

    """Submits analysis config to pipeline."""

    analysis_uuid = str(uuidlib.uuid4())

    analysis_property = Property(
        code=request_params.code,
        name=request_params.configName,
        label=request_params.label,
        description=request_params.description,
        type=request_params.design,
        data_type=request_params.dataType,
        creator_id=request_params.creatorId,
        modifier_id=request_params.modifierId,
        is_void=request_params.isVoid,
        tenant_id=request_params.tenantId,
        id=request_params.id,
        statement=request_params.statement
    )

    analysis_config_meta = PropertyMeta(
        property_id=request_params_meta.propertyId,
        code=request_params_meta.code,
        value=request_params_meta.value,
        tenant_id=request_params_meta.tenantId

    )

    analysis_config = PropertyConfig(
        order_number=request_params_config.order,
        creator_id=request_params_config.creatorId,
        is_void=request_params_config.is_void,
        property_id=request_params_config.propertyId,
        config_property_id=request_params_config.configPropertyId,
        is_layout_variable=request_params_config.isLayout,
    )


    with db.session.begin():
        # i may need to add multiple analysis config metas,
        db.session.add(analysis_property)
        db.session.add(analysis_config_meta)
        db.session.add(analysis_config)


def create_analysis_config(
    property_code, property_configName, property_label, property_description, property_design, property_data_type, property_creator_id, property_modifier_id, property_tenant_id, property_id, property_statement,
    property_meta_version, property_meta_date, property_meta_author, property_meta_email, property_meta_organization_code, property_meta_engine, property_meta_breeding_program_id,
    property_meta_pipeline_id, property_meta_stage_id, property_meta_design, property_meta_trait_level, property_meta_analysis_objective, property_meta_exp_analysis_pattern,
    property_meta_loc_analysis_pattern, property_meta_year_analysis_pattern, property_meta_trait_pattern
):
    
    #create a property
    property = Property(
        code=property_code,
        name=property_configName,
        label=property_label,
        description=property_description,
        type=property_design,
        data_type=property_data_type,
        creator_id=property_creator_id,
        modifier_id=property_modifier_id,
        is_void=False,
        tenant_id=property_tenant_id,
        id=property_id,
        statement=property_statement
    )


    #create a bunch of PropertyMeta
    property_metas = []

    property_metas.extend([
        PropertyMeta(property_id=property_id, code='Version', value=property_meta_version, tenant_id=1),
        PropertyMeta(property_id=property_id, code='date', value=property_meta_date, tenant_id=1),
        PropertyMeta(property_id=property_id, code='author', value=property_meta_author, tenant_id=1),
        PropertyMeta(property_id=property_id, code='email', value=property_meta_email, tenant_id=1),
        PropertyMeta(property_id=property_id, code='organization_code', value=property_meta_organization_code, tenant_id=1),
        PropertyMeta(property_id=property_id, code='engine', value=property_meta_engine, tenant_id=1),

        PropertyMeta(property_id=property_id, code='breeding_program_id', value=property_meta_breeding_program_id, tenant_id=1),
        PropertyMeta(property_id=property_id, code='pipeline_id', value=property_meta_pipeline_id, tenant_id=1),
        PropertyMeta(property_id=property_id, code='stage_id', value=property_meta_stage_id, tenant_id=1),
        PropertyMeta(property_id=property_id, code='design', value=property_meta_design, tenant_id=1),

        PropertyMeta(property_id=property_id, code='trait_level', value=property_meta_trait_level, tenant_id=1),
        PropertyMeta(property_id=property_id, code='analysis_objective', value=property_meta_analysis_objective, tenant_id=1),
        PropertyMeta(property_id=property_id, code='exp_analysis_pattern', value=property_meta_exp_analysis_pattern, tenant_id=1),
        PropertyMeta(property_id=property_id, code='loc_analysis_pattern', value=property_meta_loc_analysis_pattern, tenant_id=1),
        PropertyMeta(property_id=property_id, code='year_analysis_pattern', value=property_meta_year_analysis_pattern, tenant_id=1),
        PropertyMeta(property_id=property_id, code='trait_pattern', value=property_meta_trait_pattern, tenant_id=1),
    ]
    )

    #create a bunch of PropertyConfig
    analysis_config = PropertyConfig(
        order_number=999,
        creator_id=property_creator_id,
        is_void=False,
        property_id=4,
        config_property_id=property_id,
        is_layout_variable=False,
    )

    print(property_metas)

    with db.session.begin():
        db.session.add(property)
        for property_meta in property_metas:
            db.session.add(property_meta)
        db.session.add(analysis_config)



    return


# https://bitbucket.org/ebsproject/ba-db/src/develop/build/liquibase/changesets/21.09/data/template/add_2_new_models_for_cimmyt.sql?atlOrigin=eyJpIjoiMWRiZjlmZjhkYmE3NDg0Mzk3NWI3ODZhZjczNGQyODQiLCJwIjoiYmItY2hhdHMtaW50ZWdyYXRpb24ifQ