import datetime
from dataclasses import dataclass

from flask_sqlalchemy import SessionBase, SignallingSession, SQLAlchemy
from sqlalchemy.sql import func

# database instance
db = SQLAlchemy()

# models
@dataclass
class Request(db.Model):
    id: int
    uuid: str
    status: str
    tasks: list

    __tablename__ = "request"  # Base.metadata.tables["af.request"]
    __table_args__ = {"schema": "af"}

    uuid = db.Column(db.String(50))
    category = db.Column(db.String(50))
    type = db.Column(db.String(50))
    design = db.Column(db.String(50))
    requestor_id = db.Column(db.String(50))
    institute = db.Column(db.String(50))
    crop = db.Column(db.String(50))
    program = db.Column(db.String(50))
    status = db.Column(db.String(50))
    creation_timestamp = db.Column(db.DateTime, server_default=func.now())
    modification_timestamp = db.Column(db.DateTime)
    creator_id = db.Column(db.String(50))
    modifier_id = db.Column(db.String(50))
    is_void = db.Column(db.Boolean, default=False)
    tenant_id = db.Column(db.Integer)
    id = db.Column(db.Integer, primary_key=True)
    method_id = db.Column(db.Integer)
    engine = db.Column(db.String(20))
    msg = db.Column(db.String(500))

    # TODO add the other columns here
    tasks = db.relationship("Task", backref="request", foreign_keys="Task.request_id")


@dataclass
class Task(db.Model):
    id: int
    name: str
    time_start: datetime.datetime
    time_end: datetime.datetime
    status: str
    err_msg: str
    processor: str
    request_id: int

    __tablename__ = "task"
    __table_args__ = {"schema": "af"}

    name = db.Column(db.String(50))
    time_start = db.Column(db.DateTime)
    time_end = db.Column(db.DateTime)
    status = db.Column(db.String(50))
    err_msg = db.Column(db.String(500))
    processor = db.Column(db.String(50))
    tenant_id = db.Column(db.Integer, nullable=False)
    creation_timestamp = db.Column(db.DateTime, server_default=func.now())
    modification_timestamp = db.Column(db.DateTime)
    creator_id = db.Column(db.Integer, nullable=False)
    modifier_id = db.Column(db.Integer)
    is_void = db.Column(db.Boolean, nullable=False, default=False)
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey("af.request.id"))
    parent_id = db.Column(db.Integer)


@dataclass
class Property(db.Model):

    code: str
    name: str
    label: str
    description: str
    type: str
    data_type: str
    creation_timestamp: datetime.datetime
    modification_timestamp: datetime.datetime
    creator_id: str
    modifier_id: str
    id: int
    statement: str
    is_void: bool

    __tablename__ = "property"
    __table_args__ = {"schema": "af"}

    code = db.Column(db.String(50))
    name = db.Column(db.String(70))
    label = db.Column(db.String(70))
    description = db.Column(db.String(150))
    type = db.Column(db.String(50))
    data_type = db.Column(db.String(50))
    creation_timestamp = db.Column(db.DateTime)
    modification_timestamp = db.Column(db.DateTime)
    creator_id = db.Column(db.String(50))
    modifier_id = db.Column(db.String(50))
    is_void = db.Column(db.Boolean, nullable=False, default=False)
    tenant_id = db.Column(db.Integer)
    id = db.Column(db.Integer, primary_key=True)
    statement = db.Column(db.String(250))

    property_configs = db.relationship("PropertyConfig", backref="property", foreign_keys="PropertyConfig.property_id")


@dataclass
class PropertyConfig(db.Model):

    __tablename__ = "property_config"
    __table_args__ = {"schema": "af"}

    # TODO:  define columns and Foreign key here
    is_required = db.Column(db.Boolean, default=False)
    order_number = db.Column(db.Integer, default=1)
    creation_timestamp = db.Column(db.DateTime, server_default=func.now())
    modification_timestamp = db.Column(db.DateTime)
    creator_id = db.Column(db.String(50))
    modifier_id = db.Column(db.String(50))
    is_void = db.Column(db.Boolean, default=False)
    tenant_id = db.Column(db.Integer)
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey("af.property.id"))
    config_property_id = db.Column(db.Integer)
    property_ui_id = db.Column(db.Integer, db.ForeignKey("af.property_ui.id"))
    is_layout_variable = db.Column(db.Boolean, default=False)

    # relationship def one to one?
    property_ui = db.relationship("PropertyUI", backref=db.backref("property_config", uselist=False))


@dataclass
class PropertyUI(db.Model):
    __tablename__ = "property_ui"
    __table_args__ = {"schema": "af"}

    is_visible = db.Column(db.Boolean, default=True)
    minimum = db.Column(db.Integer)
    maximum = db.Column(db.Integer)
    unit = db.Column(db.String(50))
    default = db.Column(db.String(50))
    is_disabled = db.Column(db.Boolean, default=False)
    is_multiple = db.Column(db.Boolean, default=False)
    is_catalogue = db.Column(db.Boolean, default=False)
    creation_timestamp = db.Column(db.DateTime, server_default=func.now())
    modification_timestamp = db.Column(db.DateTime)
    creator_id = db.Column(db.String(50))
    modifier_id = db.Column(db.String(50))
    is_void = db.Column(db.Boolean, default=False)
    tenant_id = db.Column(db.Integer)
    id = db.Column(db.Integer, primary_key=True)
