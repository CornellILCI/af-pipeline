"""models.py"""
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.schema import ForeignKey

Base = declarative_base()
# Base.metadata.schema = "af"
# Base.metadata.reflect(db_engine)


# from the message , we should have all lthe info i need to pull model and data
# the is absolutely a way to bring in multiple classes
# the result of dg is that the info exists inside af afdb,
# and there is enough info to pull a model eg uuid
# in the case that params dont have the uuid, just hard code
# look for model id in table, but if its not

# the re
class Request(Base):
    __tablename__ = "request"  # Base.metadata.tables["af.request"]
    __table_args__ = {"schema": "af"}

    uuid = Column(String(50))
    category = Column(String(50))
    type = Column(String(50))
    design = Column(String(50))
    requestor_id = Column(String(50))
    institute = Column(String(50))
    crop = Column(String(50))
    program = Column(String(50))
    status = Column(String(50))
    creation_timestamp = Column(DateTime, server_default=func.now())
    modification_timestamp = Column(DateTime)
    creator_id = Column(String(50))
    modifier_id = Column(String(50))
    is_void = Column(Boolean, default=False)
    tenant_id = Column(Integer)
    id = Column(Integer, primary_key=True)
    method_id = Column(Integer)
    engine = Column(String(20))
    msg = Column(String(500))

    # TODO add the other columns here
    tasks = relationship("Task", backref="request")


class Task(Base):
    __tablename__ = "task"
    __table_args__ = {"schema": "af"}

    name = Column(String(50))
    time_start = Column(DateTime)
    time_end = Column(DateTime)
    status = Column(String(50))
    err_msg = Column(String(500))
    processor = Column(String(50))
    tenant_id = Column(Integer, nullable=False)
    creation_timestamp = Column(DateTime, server_default=func.now())
    modification_timestamp = Column(DateTime)
    creator_id = Column(Integer, nullable=False)
    modifier_id = Column(Integer)
    is_void = Column(Boolean, nullable=False, default=False)
    id = Column(Integer, primary_key=True)
    request_id = Column(Integer, ForeignKey("af.request.id"))
    parent_id = Column(Integer)

# create 3 separate objects

class Property(Base):
    __tablename__ = "property"  # Base.metadata.tables["af.property"]
    __table_args__ = {"schema": "af"}
    code = Column(String(50))
    name = Column(String(70))
    label = Column(String(70))
    description = Column(String(50))
    type = Column(String(50))
    data_type = Column(String(50))
    creation_timestamp = Column(DateTime, server_default=func.now())
    modification_timestamp = Column(DateTime)
    creator_id = Column(String(50))
    modifier_id = Column(String(50))
    is_void = Column(Boolean, default=False)
    tenant_id = (Column(Integer),)
    id = Column(Integer, primary_key=True)

    # TODO add the other columns here
    tasks = relationship("Task", backref="request")

class PropertyMeta(Base):
    __tablename__ = "property_meta"  # Base.metadata.tables["af.property_meta"]
    __table_args__ = {"schema": "af"}

    id = Column(Integer, primary_key=True)
    code = Column(String(50))
    creation_timestamp = Column(String(50))
    tenant_id = (Column(Integer),)
    creation_timestamp = Column(DateTime, server_default=func.now())
    modification_timestamp = Column(DateTime)
    creator_id = Column(String(50))
    modifier_id = Column(String(50))
    is_void = Column(Boolean, default=False)
    property_id = Column(Integer, primary_key=True)
    # TODO add the other columns here
    tasks = relationship("Task", backref="property_meta")



class PropertyConfig(Base):
    __tablename__ = "property_config"  # Base.metadata.tables["af.request"]
    __table_args__ = {"schema": "af"}

    is_required = Column(Boolean, default=False)
    order_number = (Column(Integer),)

    creation_timestamp = Column(DateTime, server_default=func.now())
    modification_timestamp = Column(DateTime)
    creator_id = Column(String(50))
    modifier_id = Column(String(50))

    is_void = Column(Boolean, default=False)
    tenant_id = (Column(Integer),)

    id = Column(Integer, primary_key=True)
    property_id = Column(Integer, primary_key=False)
    property_ui_id = Column(Integer,)

    config_property_id = Column(Integer, primary_key=True)
    is_layout_variable =  Column(Boolean, default=False)

    # TODO add the other columns here
    tasks = relationship("Task", backref="property_config")
