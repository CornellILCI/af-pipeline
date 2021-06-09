import uuid as uuidlib

import celery_util
from database import Property, PropertyConfig, Request, db
from flask import jsonify, render_template, request
from flask.blueprints import Blueprint
from sqlalchemy import text


def select_property_by_code(propertyCode, limit, offset):

    # sql = text((
    # #"Select Property.code, Property.name, Property.label,  "+
    # "Select Property.code, "+
    # "Property.name, "+
    # "Property.label, "+
    # "Property.description, "+
    # "Property.type, "+
    # "Property.creation_timestamp, "+
    # "Property.modification_timestamp, "+
    # "Property.creator_id, "+
    # "Property.modifier_id, "+
    # "Property.id, "+
    # "Property.statement, "+
    # "Property.is_void "+
    # "from af.Property WHERE property.id IN "+
    # "(SELECT Property_Config.config_property_id FROM af.Property "+
    # "JOIN af.Property_Config on Property_Config.property_id = Property.id "+
    # "WHERE Property.code = '{}' "+#‘trait_pattern’ "+
    # "AND Property_Config.property_id != Property_Config.config_property_id)"
    # ).format(propertyCode))
    # result = db.engine.execute(sql)
    # return result
    join_query = (
        Property.query.select_from(Property)
        .join(PropertyConfig, Property.id == PropertyConfig.property_id)
        .filter(Property.code == propertyCode, PropertyConfig.property_id != PropertyConfig.config_property_id)
    )

    subquery = join_query.with_entities(PropertyConfig.config_property_id).subquery()

    properties = Property.query.filter(Property.id.in_(subquery))
    print(str(properties))
    return properties
