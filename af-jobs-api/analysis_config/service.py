from database import Property, PropertyConfig, PropertyMeta, db
from sqlalchemy import and_, func


def get_analysis_configs(design=None):

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
    )

    # if design is not None:
    #    analysis_configs_query = analysis_configs_query.join(
    #        PropertyMeta,
    #        and_(Property.id == PropertyMeta.property_id, PropertyMeta.code == "design", PropertyMeta.value == design)
    #    )

    analysis_configs = analysis_configs_query.all()

    return analysis_configs
