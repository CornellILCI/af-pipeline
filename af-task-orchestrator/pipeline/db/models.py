from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from pipeline.db.core import Base
from sqlalchemy import Column, DateTime, Integer, String


class Request(Base):
    id: int
    uuid: str
    status: str
    tasks: list

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
    creation_timestamp = Column(DateTime)
    modification_timestamp = Column(DateTime)
    creator_id = Column(String(50))
    modifier_id = Column(String(50))
    is_void = Column(Boolean, default=False)
    tenant_id = Column(Integer)
    id = Column(Integer, primary_key=True)
    method_id = Column(Integer)
    engine = Column(String(20))
    msg = Column(String(500))


class Analysis(Base):

    __tablename__ = 'analysis'
    __table_args__ = {"schema": "af"}

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    description = Column(String(100))
    request_id = Column(Integer)
    prediction_id = Column(Integer)
    creation_timestamp = Column(DateTime)
    modification_timestamp = Column(DateTime)
    creator_id = Column(String(50))
    modifier_id = Column(String(50))
    status = Column(String)
    is_void = Column(Boolean, default=False)
    tenant_id = Column(Integer)
    model_id = Column(Integer)


class Job(Base):

    __tablename__ = 'job'
    __table_args__ = {"schema": "af"}

    id = Column(Integer, primary_key=True)
    analysis_id = Column(Integer)
    name = Column(String)
    time_start = Column(DateTime)
    time_end = Column(DateTime)
    output_path = Column(String(50))
    creation_timestamp = Column(DateTime)
    modification_timestamp = Column(DateTime)
    creator_id = Column(String(50))
    modifier_id = Column(String(50))
    status = Column(String)
    status_message = Column(String)
    is_void = Column(Boolean, default=False)
    tenant_id = Column(Integer)


class Property(Base):

    __tablename__ = "property"
    __table_args__ = {"schema": "af"}

    id = Column(Integer, primary_key=True)
    code = Column(String(50))
    name = Column(String(70))
    label = Column(String(70))
    description = Column(String(50))
    type = Column(String(50))
    data_type = Column(String(50))
    creation_timestamp = Column(DateTime)
    modification_timestamp = Column(DateTime)
    creator_id = Column(String(50))
    modifier_id = Column(String(50))
    is_void = Column(Boolean, default=False)
    tenant_id = Column(Integer)
    statement = Column(String(250))
    

class PropertyMeta(Base):
    __tablename__ = "property_meta"
    __table_args__ = {"schema": "af"}

    id = Column(Integer, primary_key=True)
    code = Column(String(30))
    value = Column(String(255))
    tenant_id = Column(Integer)
    creation_timestamp = Column(DateTime)
    modification_timestamp = Column(DateTime)
    creator_id = Column(String(50))
    modifier_id = Column(String(50))
    is_void = Column(Boolean, default=False)
    property_id = Column(Integer)

class PropertyConfig(Base):
    __tablename__ = "property_config"
    __table_args__ = {"schema": "af"}
    
    id = Column(Integer, primary_key=True)

    is_required = Column(Boolean, default=False)
    order_number = Column(Integer)

    creation_timestamp = Column(DateTime)
    modification_timestamp = Column(DateTime)
    creator_id = Column(String(50))
    modifier_id = Column(String(50))

    is_void = Column(Boolean, default=False)
    tenant_id = Column(Integer)

    property_id = Column(Integer, ForeignKey('af.property.id'))
    property_ui_id = Column(Integer,)

    config_property_id = Column(Integer)
    is_layout_variable =  Column(Boolean, default=False)


