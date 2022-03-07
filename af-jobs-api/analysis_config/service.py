import json

from database import Property, PropertyConfig, PropertyMeta, db
from sqlalchemy import and_, func


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
