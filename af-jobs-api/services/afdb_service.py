import uuid as uuidlib

import celery_util
from database import Request, db
from flask import jsonify, render_template, request
from flask.blueprints import Blueprint
from sqlalchemy import text

def select_analysis_configs(analysisConfigID, limit, offset, configType):
    
    sql = text((
        "SELECT "+
        "formula_property.code, "+
        "formula_property.label, "+
        "formula_property.description, "+
        "formula_property.type, "+
        "formula_property.data_type, "+
        "formula_property.creation_timestamp, "+
        "formula_property.modification_timestamp, "+
        "formula_property.creator_id, "+
        "formula_property.modifier_id, "+
        "formula_property.is_void, "+
        "formula_property.tenant_id, "+
        "formula_property.statement, "+
        "property_config.property_id, "+
        "formula_property.name "+
        "FROM af.property_config "+
        "INNER JOIN af.property_config AS formula_configs "+
        "ON formula_configs.property_id = (SELECT property.id FROM af.property WHERE code = '{}') "+
        "AND formula_configs.config_property_id = property_config.config_property_id "+
        "AND property_config.property_id = {} "+
        "INNER JOIN af.property AS formula_property "+
        "ON formula_property.id = formula_configs.config_property_id "+
        "LIMIT {} OFFSET {} "
    ).format(configType, analysisConfigID, limit, offset))
    result = db.engine.execute(sql)
    return result