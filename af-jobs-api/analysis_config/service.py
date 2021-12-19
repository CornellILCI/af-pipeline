from database import Property, PropertyConfig
from sqlalchemy import and_

def get_analysis_configs():

    analysis_config_base_property = Property.query.filter(Property.code == "analysis_config").one()

    analysis_configs = (
        Property.query.select_from(PropertyConfig)
        .join(
            Property,
            and_(
                Property.id == PropertyConfig.config_property_id,
                Property.id != analysis_config_base_property.id,
                PropertyConfig.property_id == analysis_config_base_property.id,
            ),
        )
        .all()
    )

    return analysis_configs
