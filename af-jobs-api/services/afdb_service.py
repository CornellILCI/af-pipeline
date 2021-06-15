import uuid as uuidlib

import celery_util
from database import Property, PropertyConfig, Request, db
from flask import jsonify, render_template, request
from flask.blueprints import Blueprint
from sqlalchemy import text


def select_property_by_code(propertyCode, limit, offset):

    join_query = (
        Property.query.select_from(Property)
        .join(PropertyConfig, Property.id == PropertyConfig.property_id)
        .filter(Property.code == propertyCode, PropertyConfig.property_id != PropertyConfig.config_property_id)
    )

    subquery = join_query.with_entities(PropertyConfig.config_property_id).subquery()

    properties = Property.query.filter(Property.id.in_(subquery))
    print(str(properties))
    return properties
