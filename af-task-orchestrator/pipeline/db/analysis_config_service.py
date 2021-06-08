from pipeline.db.models import Property, PropertyConfig, PropertyMeta
from sqlalchemy.orm import aliased
from sqlalchemy import and_

def get_analysis_config(db_session, analysis_config_id: int) -> Property:
    formula = self.db_session.query(Property).get(analysis_config_id)


def get_analysis_config_properties(db_session, analysis_config_id: int, property_code: str) -> list[Property]:
    
    _analysis_config_property_configs = aliased(PropertyConfig)    

    child_property_root = db_session.query(Property).filter(Property.code == property_code).one()

    properties = (
            db_session
            .query(Property)
            .select_from(PropertyConfig)
            .join(_analysis_config_property_configs, and_(
                PropertyConfig.property_id == child_property_root.id,
                PropertyConfig.config_property_id == _analysis_config_property_configs.config_property_id,
                _analysis_config_property_configs.property_id == analysis_config_id))
            .join(Property, Property.id == PropertyConfig.config_property_id)
            .all())

    return properties
