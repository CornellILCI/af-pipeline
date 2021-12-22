from database import Property, PropertyConfig, PropertyMeta, db
from sqlalchemy import and_, func

import json


def get_analysis_configs(design=None):
    
    query_params = {}

    if design is not None:
        query_params["design"] = [design]

    analysis_config_base_property = Property.query.filter(Property.code == "analysis_config").one()

    analysis_configs_query = (
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
    
    analysis_config_code_value_agg_q = (
        db.session
        .query(analysis_configs_query.c.id)
        .group_by(analysis_configs_query.c.id)
        .having(func.jsonb_object_agg(analysis_configs_query.c.code, analysis_configs_query.c.meta_value)
            .op("@>")(json.dumps(query_params))
        )
        .subquery()
    )

    analysis_configs = db.session.query(Property).filter(Property.id.in_(analysis_config_code_value_agg_q)).all()

    return analysis_configs
